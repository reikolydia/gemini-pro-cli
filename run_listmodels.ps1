Clear-Host

. "C:\Program Files\Python310\python.exe" -m venv google_pro_cli

$venvpath = $pwd.path + "\google_pro_cli\Scripts\Activate.ps1"

. $venvpath

pip install -r requirements.txt
python -m pip install --upgrade pip

$api_key = Read-Host "Input Google AI Studio API key"

$env = "GENAI_API_KEY=" + $api_key

$env > .env

Clear-Host

python listmodels.py

deactivate
