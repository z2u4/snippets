import * as vscode from 'vscode'
import { MasscodeAPI } from '../api'
import type { Snippet, SnippetContent } from '../types'

export class SnippetsProvider implements vscode.TreeDataProvider<Snippet | SnippetContent>, vscode.TextDocumentContentProvider {
  private _onDidChangeTreeData = new vscode.EventEmitter<Snippet | SnippetContent | undefined | null | void>()
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event

  // For document content provider
  private _onDidChange = new vscode.EventEmitter<vscode.Uri>()
  readonly onDidChange = this._onDidChange.event

  // Track opened fragments with index
  private openedFragments = new Map<string, {
    snippetId: string
    fragmentName: string
    content: string
    index: number
  }>()

  // Scheme for our custom URIs
  static readonly scheme = 'masscode'

  // New method to handle all registrations
  register (context: vscode.ExtensionContext): void {
    // Register document provider
    context.subscriptions.push(
      vscode.workspace.registerTextDocumentContentProvider(SnippetsProvider.scheme, this)
    )

    // Register commands
    context.subscriptions.push(
      vscode.commands.registerCommand('masscodepp.openFragment', this.openFragment.bind(this)),
      vscode.commands.registerCommand('masscodepp.refreshSnippets', () => this.refresh())
    )
  }

  // TextDocumentContentProvider implementation
  provideTextDocumentContent (uri: vscode.Uri): string {
    const fragmentInfo = this.openedFragments.get(uri.toString())
    return fragmentInfo?.content || ''
  }

  // Create a custom URI for a fragment with index
  private getFragmentUri (snippetId: string, fragmentName: string, index: number): vscode.Uri {
    return vscode.Uri.parse(`${SnippetsProvider.scheme}:${snippetId}/${index}/${fragmentName}`)
  }

  async openFragment (fragment: SnippetContent, parentSnippetId: string, index: number): Promise<void> {
    const uri = this.getFragmentUri(parentSnippetId, fragment.label, index)

    // Store fragment information with index
    this.openedFragments.set(uri.toString(), {
      snippetId: parentSnippetId,
      fragmentName: fragment.label,
      content: fragment.value,
      index
    })

    // Open the document
    const doc = await vscode.workspace.openTextDocument(uri)
    await vscode.window.showTextDocument(doc)

    // Set the language mode
    let targetLanguage = fragment.language
    if (targetLanguage === 'plain_text') {
      targetLanguage = 'plaintext'
    }

    await vscode.languages.setTextDocumentLanguage(doc, targetLanguage) // Fixed to use targetLanguage instead of fragment.language
  }

  // TreeDataProvider implementation remains mostly the same
  refresh (): void {
    this._onDidChangeTreeData.fire()
  }

  getTreeItem (element: Snippet | SnippetContent): vscode.TreeItem {
    if ('content' in element) {
      return {
        label: element.name || 'Untitled Snippet',
        collapsibleState: vscode.TreeItemCollapsibleState.Collapsed,
        tooltip: `${element.folder?.name || 'Inbox'}`,
        description: element.folder?.name || 'Inbox'
      }
    } else {
      return {
        label: element.label || 'Untitled Fragment',
        collapsibleState: vscode.TreeItemCollapsibleState.None,
        tooltip: element.language,
        description: element.language,
        command: {
          command: 'masscodepp.openFragment',
          title: 'Open Fragment',
          arguments: [element, (element as any).parentSnippetId, (element as any).index]
        }
      }
    }
  }

  async getChildren (element?: Snippet | SnippetContent): Promise<(Snippet | SnippetContent)[]> {
    if (!element) {
      return await MasscodeAPI.getAllSnippets()
    } else if ('content' in element) {
      return element.content.map(fragment => ({
        ...fragment,
        parentSnippetId: element.id,
        index: element.content.indexOf(fragment)
      }))
    }
    return []
  }

  // Helper method to get fragment info now includes index
  getFragmentInfo (uri: vscode.Uri): {
    snippetId: string
    fragmentName: string
    index: number
  } | undefined {
    return this.openedFragments.get(uri.toString())
  }
}
