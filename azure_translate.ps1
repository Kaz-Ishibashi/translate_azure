$output = "sbj\" + $Args[0] + "_translated.txt"
python azure.py $Args[0]

#Write-Output "translating $Args[0].txt to Japanese..."
#Start-Sleep -s 2
Write-Output "translation completed."

Get-Content -Encoding Shift-JIS $output|Set-clipboard