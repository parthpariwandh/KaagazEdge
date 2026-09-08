Set-ExecutionPolicy -Scope CurrentUser Unrestricted -Force
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "KaagazEdge venv ready. Place Qualcomm AI Hub ONNX artifacts in .\models before NPU runs."
