$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $RootDir 'WHITEPAPER.md'
$OutputDir = Join-Path $RootDir 'dist'

if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    throw '未找到pandoc，无法构建。'
}

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
$Html = Join-Path $OutputDir 'AI原生开放助农网络白皮书.html'
& pandoc $Source --standalone --toc --metadata 'title=AI原生开放助农网络白皮书' -o $Html

if (Get-Command xelatex -ErrorAction SilentlyContinue) {
    $Pdf = Join-Path $OutputDir 'AI原生开放助农网络白皮书.pdf'
    & pandoc $Source --toc --pdf-engine=xelatex -V documentclass=ctexbook -V classoption=oneside -o $Pdf
} else {
    Write-Host '未找到xelatex，已跳过PDF，仅生成HTML。'
}

Write-Host "构建完成：$OutputDir"
