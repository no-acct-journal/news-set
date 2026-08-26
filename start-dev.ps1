$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Frontend = Join-Path $Root "frontend"
$BackendEnv = Join-Path $Root ".env"
$FrontendEnv = Join-Path $Frontend ".env"
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

function Require-Command {
    param(
        [string]$Name,
        [string]$Hint
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "$Name was not found. $Hint"
    }
}

function Invoke-PostgresSql {
    param([string]$File)

    Get-Content -Raw $File | docker compose exec -T postgres psql -U postgres -d news_set
}

Set-Location $Root

Require-Command "docker" "Install Docker Desktop and make sure it is running."
Require-Command "npm.cmd" "Install Node.js LTS."

if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    if (Get-Command "py" -ErrorAction SilentlyContinue) {
        $PythonCommand = "py"
    } else {
        throw "python was not found. Install Python 3.10+."
    }
} else {
    $PythonCommand = "python"
}

if (-not (Test-Path $BackendEnv)) {
    Copy-Item (Join-Path $Root ".env.example") $BackendEnv
    Write-Host "Created backend .env from .env.example"
}

if (-not (Test-Path $FrontendEnv)) {
    Copy-Item (Join-Path $Frontend ".env.example") $FrontendEnv
    Write-Host "Created frontend .env from frontend/.env.example"
}

Write-Host "Starting PostgreSQL and Redis with Docker Compose..."
docker compose up -d postgres redis

Write-Host "Waiting for PostgreSQL..."
$DatabaseReady = $false
for ($i = 0; $i -lt 30; $i++) {
    docker compose exec -T postgres pg_isready -U postgres -d news_set | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $DatabaseReady = $true
        break
    }
    Start-Sleep -Seconds 2
}

if (-not $DatabaseReady) {
    throw "PostgreSQL did not become ready in time."
}

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating Python virtual environment..."
    & $PythonCommand -m venv .venv
}

Write-Host "Installing backend dependencies..."
& $VenvPython -m pip install -r requirements.txt

Write-Host "Applying database schema..."
Invoke-PostgresSql (Join-Path $Root "database\schema.sql")

Write-Host "Loading example seed data..."
Invoke-PostgresSql (Join-Path $Root "database\seed.example.sql")

Write-Host "Installing frontend dependencies..."
Push-Location $Frontend
npm.cmd install
Pop-Location

$BackendCommand = "Set-Location '$Root'; & '$VenvPython' -m uvicorn main:app --reload"
$FrontendCommand = "Set-Location '$Frontend'; npm.cmd run dev"

Write-Host "Starting backend at http://127.0.0.1:8000"
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $BackendCommand

Write-Host "Starting frontend at http://127.0.0.1:5173"
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $FrontendCommand

Write-Host ""
Write-Host "News Set is starting."
Write-Host "Frontend: http://127.0.0.1:5173"
Write-Host "API docs:  http://127.0.0.1:8000/docs"
