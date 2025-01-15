import * as vscode from 'vscode'
import axios from 'axios'
import type { Snippet, Tag, Folder } from './types'

export class MasscodeAPI {
  public static getApiUrl (): string {
    const apiUrl = vscode.workspace.getConfiguration('masscodepp').get('apiUrl')
    if (!apiUrl) {
      return 'http://localhost:3033'
    }
    return apiUrl as string
  }

  static async getAllTags (): Promise<Tag[]> {
    const { data } = await axios.get<Tag[]>(`${this.getApiUrl()}/tags`)
    return data
  }

  static async getAllFolders (): Promise<Folder[]> {
    const { data } = await axios.get<Folder[]>(`${this.getApiUrl()}/folders`)
    return data
  }

  static buildParams (): string {
    const preferences = vscode.workspace.getConfiguration('masscodepp')
    // const tagFilters = vscode.workspace.getConfiguration('masscodepp.tagFilter').get('tags', [])
    // const folderFilter = vscode.workspace.getConfiguration('masscodepp.folderFilter').get('folders', [])
    // const tagInclude = vscode.workspace.getConfiguration('masscodepp.tagFilter').get('type', 'include') === 'include'
    // const folderInclude = vscode.workspace.getConfiguration('masscodepp.folderFilter').get('type', 'include') === 'include'
    const moreFilters = preferences.get('moreFilters') || {}
    let params = '?'
    for (const [key, value] of Object.entries(moreFilters)) {
      params += `${key}=${value}&`
    }
    return params
  }

  static async getAllSnippets (
    filterMeta?: {
      tagFilter: {
        type: string
        tags: string[]
      }
      folderFilter: {
        type: string
        folders: string[]
      }
      moreFilters: object
    }
  ): Promise<Snippet[]> {
    try {
      const { data } = await axios.get<Snippet[]>(
        `${this.getApiUrl()}/snippets/embed-folder`
      )
      return data
        .filter(snippet => !snippet.isDeleted)
        .sort((a, b) => (a.createdAt > b.createdAt ? -1 : 1))
    } catch (err) {
      vscode.window.showErrorMessage(String(err))
      return []
    }
  }
}
