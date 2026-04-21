
# wiki_repair.ps1
$wikiDir = "d:\LLM Wiki DHCHO\wiki"
$mappingJson = Get-Content -Path "d:\LLM Wiki DHCHO\scratch\link_mapping.json" -Raw | ConvertFrom-Json

$files = Get-ChildItem -Path $wikiDir -Filter "*.md"

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding utf8
        $changed = $false
        
        # We look for [[Link]] patterns
        # We use a regex to find all links and check if they are in the mapping
        $newContent = [regex]::Replace($content, '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', {
            param($match)
            $linkName = $match.Groups[1].Value.Trim()
            # Note: link_mapping.json property names with special chars need access via PSObject or similar
            # But simple way is to check the NoteProperty names
            $mappedValue = $mappingJson.PSObject.Properties[$linkName].Value
            if ($mappedValue) {
                $changed = $true
                return "[[${mappedValue}]]"
            } else {
                return $match.Value
            }
        })
        
        if ($changed) {
            Write-Host "Repairing links in: $($file.Name)"
            $newContent | Set-Content -Path $file.FullName -Encoding utf8
        }
    } catch {
        Write-Warning "Failed to process $($file.Name): $($_.Exception.Message)"
    }
}

Write-Host "Wiki Link Repair Complete!"
