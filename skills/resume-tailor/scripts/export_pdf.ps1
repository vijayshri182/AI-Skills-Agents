# Export a .docx to PDF using Microsoft Word (COM). Prints the page count.
#
# Usage:
#   powershell -File export_pdf.ps1 -In "Tailored.docx" -Out "Tailored.pdf"
#
param(
    [Parameter(Mandatory = $true)][string]$In,
    [Parameter(Mandatory = $true)][string]$Out
)

$ErrorActionPreference = "Stop"
$In = (Resolve-Path -LiteralPath $In).Path
$Out = [System.IO.Path]::GetFullPath($Out)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $null
try {
    # Open read-only, without prompting to convert
    $doc = $word.Documents.Open($In, $false, $true)
    # wdExportFormatPDF = 17 ; export with bookmarks + document structure
    $doc.ExportAsFixedFormat($Out, 17, $false, 0, 0, 0, 0, 0, $true, $true, 0, $true, $true, $false)
    $pages = $doc.ComputeStatistics(2)  # wdStatisticPages = 2
    Write-Output "PDF: $Out"
    Write-Output "Pages: $pages"
}
finally {
    if ($doc) { $doc.Close($false) }
    try { $word.Quit() } catch { }
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
