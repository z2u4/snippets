import * as vscode from 'vscode'
import * as path from 'path'

export async function settingCommand () {
  try {
    const workspaceFolders = vscode.workspace.workspaceFolders

    if (!workspaceFolders) {
      throw new Error('No workspace folder found')
    }

    const settingsPath = path.join(workspaceFolders[0].uri.fsPath, '.vscode', 'settings.json')
    const settingsUri = vscode.Uri.file(settingsPath)

    // Ensure .vscode folder and settings.json exist with masscodepp config
    await ensureSettings(settingsUri)

    // Open settings.json
    const document = await vscode.workspace.openTextDocument(settingsUri)
    await vscode.window.showTextDocument(document)
  } catch (err) {
    vscode.window.showErrorMessage('Failed to open workspace settings')
  }
}

async function ensureSettings (settingsUri: vscode.Uri) {
  try {
    // Try to read existing settings
    await vscode.workspace.fs.stat(settingsUri)
    const document = await vscode.workspace.openTextDocument(settingsUri)
    const settings = JSON.parse(document.getText())

    // Add masscodepp if it doesn't exist
    if (!settings.masscodepp) {
      settings.masscodepp = {}

      // Write back the updated settings
      const content = JSON.stringify(settings, null, 2)
      await vscode.workspace.fs.writeFile(settingsUri, Buffer.from(content))
    }
  } catch {
    // If settings.json doesn't exist, create it with masscodepp config
    const defaultSettings = {
      masscodepp: {}
    }

    // Create .vscode folder if it doesn't exist
    await vscode.workspace.fs.createDirectory(vscode.Uri.file(path.dirname(settingsUri.fsPath)))

    // Write initial settings
    const content = JSON.stringify(defaultSettings, null, 2)
    await vscode.workspace.fs.writeFile(settingsUri, Buffer.from(content))
  }
}
