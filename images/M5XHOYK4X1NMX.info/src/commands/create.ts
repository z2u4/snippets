import * as vscode from 'vscode'
import axios from 'axios'
import type { Snippet } from '../types'
import { MasscodeAPI } from '../api'

export async function createCommand () {
  const editor = vscode.window.activeTextEditor
  if (!editor) {
    return
  }

  const selection = editor.selection
  const content = editor.document.getText(selection)

  let language = editor.document.languageId

  if (language === 'plaintext') {
    language = 'plain_text'
  }

  if (content.length <= 1) return

  const isNotify = vscode.workspace.getConfiguration('masscodepp').get('notify')
  const apiUrl = await MasscodeAPI.getApiUrl()

  const name = await vscode.window.showInputBox()
  const snippet: Partial<Snippet> = {
    name,
    content: [
      {
        label: 'Fragment 1',
        value: content,
        language
      }
    ]
  }

  try {
    await axios.post(`${apiUrl}/snippets/create`, snippet)
    if (isNotify) {
      vscode.window.showInformationMessage('Snippet successfully created')
    }
  } catch (err) {
    vscode.window.showErrorMessage('massCode app is not running.')
  }
}
