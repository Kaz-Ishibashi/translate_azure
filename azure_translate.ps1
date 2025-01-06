$output = "sbj\" + $Args[0] + "_translated.txt"
Write-Output "translating $Args[0].txt to Japanese..."

python azure.py $Args[0]

#Start-Sleep -s 2
#Write-Output "translation completed."

# クリップボードにコピー
Get-Content -Encoding Shift-JIS $output|Set-clipboard