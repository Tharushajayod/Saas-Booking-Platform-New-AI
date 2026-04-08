# PowerShell script to run and test the full app stack locally (Windows)
# Usage: powershell -ExecutionPolicy Bypass -File .\scripts\run_local_tests.ps1

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Working dir: $PWD"

function Wait-ForHttp {
    param(
        [string]$Url,
        [int]$TimeoutSec = 120,
        [int]$IntervalSec = 3
    )
    $start = Get-Date
    while ((Get-Date) - $start).TotalSeconds -lt $TimeoutSec {
        try {
            $r = curl.exe -sS $Url 2>$null
            if ($LASTEXITCODE -eq 0 -and $r) {
                Write-Host "HTTP OK: $Url"
                return $r
            }
        } catch {
            # ignore
        }
        Start-Sleep -Seconds $IntervalSec
        Write-Host "Waiting for $Url..."
    }
    throw "Timeout waiting for $Url"
}

Write-Host "1/10: Building and starting containers (detached)"
docker compose up --build -d

Write-Host "2/10: Waiting for backend health endpoint"
try {
    $health = Wait-ForHttp -Url 'http://localhost:8000/api/auth/health/' -TimeoutSec 180 -IntervalSec 3
    Write-Host "Backend health: $health"
} catch {
    Write-Error "Backend health check failed: $_"
    docker compose logs backend --tail 200 | Out-File -FilePath "$root/backend_logs_startup.txt" -Encoding utf8
    exit 1
}

Write-Host "3/10: Applying migrations"
docker compose exec backend python manage.py migrate --noinput

Write-Host "4/10: Ensure superuser exists"
docker compose exec backend python /app/scripts/create_superuser.py || Write-Host 'create_superuser returned nonzero'

Write-Host "5/10: Seed demo property/room/booking"
docker compose exec backend python /app/scripts/create_property_for_owner.py || Write-Host 'create_property_for_owner returned nonzero'
docker compose exec backend python /app/scripts/create_room_for_property.py || Write-Host 'create_room_for_property returned nonzero'
docker compose exec backend python /app/scripts/create_booking_for_room.py || Write-Host 'create_booking_for_room returned nonzero'

Write-Host "6/10: Run automated API smoke tests (inside container)"
docker compose exec backend python /app/scripts/api_tests.py 2>&1 | Tee-Object -FilePath "$root/backend_api_tests.log"

Write-Host "7/10: Capture backend logs"
docker compose logs backend --tail 200 > "$root/backend_logs_after_tests.txt"

Write-Host "8/10: Check frontend root (host port 3001)"
try {
    $frontendRoot = Wait-ForHttp -Url 'http://localhost:3001/' -TimeoutSec 60 -IntervalSec 3
    $frontendRoot | Out-File -FilePath "$root/frontend_root.html" -Encoding utf8
    Write-Host "Frontend root saved to frontend_root.html"
} catch {
    Write-Warning "Frontend health check failed: $_"
}

Write-Host "9/10: Check backend health again"
try { Wait-ForHttp -Url 'http://localhost:8000/api/auth/health/' -TimeoutSec 30 -IntervalSec 2 | Out-File -FilePath "$root/backend_health_after.txt" -Encoding utf8 } catch { Write-Warning "Backend final health check failed" }

Write-Host "10/10: Finished. Logs and test output written to project root: backend_api_tests.log, backend_logs_after_tests.txt, backend_health_after.txt, frontend_root.html"

exit 0
