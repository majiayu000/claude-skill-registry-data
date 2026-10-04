---
name: storage_ui_spec
description: STORAGE UI SPEC
---

# STORAGE UI SPEC

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **STORAGE UI SPEC**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/angel solutions site/internet_archive_master/prometheus-archive-engine-v3.1-STORAGE-STRIPE-COMPLETE/prometheus-archive-engine/docs/STORAGE_UI_SPEC.md`

## 🧠 Master Agent Prompt & Capabilities

# 🗄️ STORAGE SYSTEM UI SPECIFICATIONS
## Complete File Management Interface

**Tech Stack**: Next.js 16.2 + React 19.2 + Tailwind 4.2 + shadcn/ui v4

═══════════════════════════════════════════════════════════════════
## 📦 STORAGE DASHBOARD (`/storage`)
═══════════════════════════════════════════════════════════════════

### **Layout**
```tsx
<StorageDashboard>
  {/* Left Sidebar */}
  <StorageSidebar>
    <StorageUsage
      used={2.3}
      total={10}
      unit="GB"
      percentage={23}
    />
    
    <FolderTree
      folders={[
        {id: "root", name: "My Files", children: [...]},
        {id: "shared", name: "Shared with me", children: [...]},
        {id: "recent", name: "Recent", virtual: true},
        {id: "starred", name: "Starred", virtual: true},
        {id: "trash", name: "Trash", virtual: true}
      ]}
      onFolderClick={navigateToFolder}
    />
    
    <QuickFilters>
      <FilterButton icon="Image" label="Images" />
      <FilterButton icon="Video" label="Videos" />
      <FilterButton icon="FileText" label="Documents" />
      <FilterButton icon="Music" label="Audio" />
      <FilterButton icon="Archive" label="Archives" />
      <FilterButton icon="Code" label="Code" />
    </QuickFilters>
  </StorageSidebar>
  
  {/* Main Content */}
  <MainContent>
    {/* Toolbar */}
    <Toolbar>
      <UploadButton
        onUpload={handleUpload}
        accept="*/*"
        multiple={true}
        dragDrop={true}
      />
      
      <NewFolderButton onClick={createFolder} />
      
      <ViewToggle
        value={viewMode}
        options={["grid", "list", "preview"]}
        onChange={setViewMode}
      />
      
      <SearchBar
        placeholder="Search files..."
        onSearch={searchFiles}
        filters={["name", "content", "tags"]}
      />
      
      <SortDropdown
        options={[
          "Name (A-Z)",
          "Name (Z-A)",
          "Date (Newest)",
          "Date (Oldest)",
          "Size (Largest)",
          "Size (Smallest)",
          "Type"
        ]}
        onChange={setSortOrder}
      />
    </Toolbar>
    
    {/* Breadcrumb */}
    <Breadcrumb
      path={["My Files", "Projects", "2026", "Archive"]}
      onNavigate={navigateToPath}
    />
    
    {/* File Grid/List */}
    {viewMode === "grid" && (
      <FileGrid>
        {files.map(file => (
          <FileCard
            key={file.id}
            file={file}
            thumbnail={file.thumbnail_url}
            name={file.original_filename}
            size={formatFileSize(file.file_size)}
            type={file.file_type}
            date={formatDate(file.created_at)}
            starred={file.starred}
            shared={file.visibility === "shared"}
            onSelect={selectFile}
            onPreview={previewFile}
            onDownload={downloadFile}
            onShare={shareFile}
            onDelete={deleteFile}
            onStar={toggleStar}
            contextMenu={[
              {icon: "Eye", label: "Preview", action: previewFile},
              {icon: "Download", label: "Download", action: downloadFile},
              {icon: "Share", label: "Share", action: shareFile},
              {icon: "Copy", label: "Copy link", action: copyLink},
              {icon: "Tag", label: "Add tags", action: addTags},
              {icon: "FolderOpen", label: "Move to", action: moveFile},
              {icon: "Clock", label: "Version history", action: showVersions},
              {separator: true},
              {icon: "Trash", label: "Delete", action: deleteFile, danger: true}
            ]}
          />
        ))}
      </FileGrid>
    )}
    
    {viewMode === "list" && (
      <FileList>
        <DataTable
          columns={[
            {key: "thumbnail", label: "", width: 40, render: renderThumbnail},
            {key: "name", label: "Name", sortable: true, width: "40%"},
            {key: "type", label: "Type", sortable: true, width: 100},
            {key: "size", label: "Size", sortable: true, width: 100},
            {key: "modified", label: "Modified", sortable: true, width: 150},
            {key: "shared", label: "Shared", width: 80, render: renderShared},
            {key: "actions", label: "", width: 100, render: renderActions}
          ]}
          data={files}
          selectable={true}
          onRowClick={previewFile}
          onRowSelect={selectFile}
        />
      </FileList>
    )}
    
    {/* Bulk Actions Bar (appears when files selected) */}
    {selectedFiles.length > 0 && (
      <BulkActionsBar
        count={selectedFiles.length}
        actions={[
          {icon: "Download", label: "Download", onClick: downloadSelected},
          {icon: "Archive", label: "Archive", onClick: archiveSelected},
          {icon: "FolderOpen", label: "Move", onClick: moveSelected},
          {icon: "Tag", label: "Tag", onClick: tagSelected},
          {icon: "Share", label: "Share", onClick: shareSelected},
          {icon: "Trash", label: "Delete", onClick: deleteSelected}
        ]}
        onClear={clearSelection}
      />
    )}
  </MainContent>
  
  {/* Right Panel (Details) */}
  <DetailsPanel>
    {selectedFile && (
      <>
        <FileThumbnail
          file={selectedFile}
          size="large"
          interactive={true}
        />
        
        <FileDetails>
          <DetailRow label="Name" value={selectedFile.original_filename} editable />
          <DetailRow label="Type" value={selectedFile.file_type} />
          <DetailRow label="Size" value={formatFileSize(selectedFile.file_size)} />
          <DetailRow label="Created" value={formatDate(selectedFile.created_at)} />
          <DetailRow label="Modified" value={formatDate(selectedFile.updated_at)} />
          <DetailRow label="Downloads" value={selectedFile.download_count} />
          <DetailRow label="Checksum" value={selectedFile.checksum} copyable />
        </FileDetails>
        
        <TagEditor
          tags={selectedFile.tags}
          onAdd={addTag}
          onRemove={removeTag}
        />
        
        <VisibilitySettings>
          <RadioGroup
            value={selectedFile.visibility}
            options={[
              {value: "private", label: "Private", icon: "Lock"},
              {value: "shared", label: "Shared", icon: "Users"},
              {value: "public", label: "Public", icon: "Globe"}
            ]}
            onChange={updateVisibility}
          />
          
          {selectedFile.visibility === "shared" && (
            <ShareWithUsers
              sharedWith={selectedFile.shared_with}
              onAdd={addSharedUser}
              onRemove={removeSharedUser}
            />
          )}
        </VisibilitySettings>
        
        <VersionHistory
          versions={fileVersions}
          currentVersion={selectedFile.version}
          onRestore={restoreVersion}
          onCompare={compareVersions}
        />
        
        <ActionButtons>
          <Button onClick={downloadFile}>
            <Download className="w-4 h-4 mr-2" />
            Download
          </Button>
          <Button onClick={shareFile} variant="outline">
            <Share className="w-4 h-4 mr-2" />
            Share
          </Button>
          <Button onClick={deleteFile} variant="destructive">
            <Trash className="w-4 h-4 mr-2" />
            Delete
          </Button>
        </ActionButtons>
      </>
    )}
  </DetailsPanel>
</StorageDashboard>
```

═══════════════════════════════════════════════════════════════════
## ⬆️ UPLOAD INTERFACE
═══════════════════════════════════════════════════════════════════

### **Drag & Drop Upload**
```tsx
<UploadZone
  onDrop={handleDrop}
  multiple={true}
  maxSize={5 * 1024 * 1024 * 1024}  // 5 GB
  accept="*/*"
>
  <UploadIcon className="w-16 h-16 text-muted-foreground" />
  <h3>Drag files here or click to browse</h3>
  <p>Maximum file size: 5 GB</p>
  
  <input
    type="file"
    multiple
    onChange={handleFileSelect}
    className="hidden"
    id="file-upload"
  />
</UploadZone>

{/* Upload Progress */}
{uploads.map(upload => (
  <UploadProgress
    key={upload.id}
    filename={upload.filename}
    progress={upload.progress}
    speed={upload.speed}
    eta={upload.eta}
    status={upload.status}
    onCancel={() => cancelUpload(upload.id)}
    onRetry={() => retryUpload(upload.id)}
  />
))}
```

### **Upload Queue Manager**
```tsx
<UploadQueueManager>
  <QueueHeader>
    <h3>Uploads ({queue.length})</h3>
    <Button onClick={pauseAll}>Pause All</Button>
    <Button onClick={resumeAll}>Resume All</Button>
    <Button onClick={clearCompleted}>Clear Completed</Button>
  </QueueHeader>
  
  <QueueList>
    {queue.map(item => (
      <QueueItem
        file={item.file}
        status={item.status}
        progress={item.progress}
        error={item.error}
        onPause={pauseUpload}
        onResume={resumeUpload}
        onCancel={cancelUpload}
      />
    ))}
  </QueueList>
</UploadQueueManager>
```

═══════════════════════════════════════════════════════════════════
## 🔗 SHARE DIALOG
═══════════════════════════════════════════════════════════════════

```tsx
<ShareDialog file={selectedFile} open={shareDialogOpen} onClose={closeShareDialog}>
  <DialogHeader>
    <DialogTitle>Share "{selectedFile.original_filename}"</DialogTitle>
  </DialogHeader>
  
  <TabsContainer>
    {/* Share Link Tab */}
    <Tab label="Share Link">
      <ShareLinkGenerator>
        <Input
          value={shareLink}
          readOnly
          suffix={
            <Button onClick={copyShareLink} size="sm">
              <Copy className="w-4 h-4" />
            </Button>
          }
        />
        
        <ShareOptions>
          <div className="flex items-center justify-between">
            <Label>Password Protection</Label>
            <Switch checked={requirePassword} onChange={setRequirePassword} />
          </div>
          
          {requirePassword && (
            <Input
              type="password"
              placeholder="Enter password"
              value={sharePassword}
              onChange={setSharePassword}
            />
          )}
          
          <div className="flex items-center justify-between">
            <Label>Expiration</Label>
            <Select
              value={expiresIn}
              options={[
                {value: "1h", label: "1 hour"},
                {value: "24h", label: "24 hours"},
                {value: "7d", label: "7 days"},
                {value: "30d", label: "30 days"},
                {value: "never", label: "Never"}
              ]}
              onChange={setExpiresIn}
            />
          </div>
          
          <div className="flex items-center justify-between">
            <Label>Download Limit</Label>
            <Input
              type="number"
              placeholder="Unlimited"
              value={maxDownloads}
              onChange={setMaxDownloads}
            />
          </div>
        </ShareOptions>
        
        <Button onClick={generateShareLink} className="w-full">
          Generate Link
        </Button>
      </ShareLinkGenerator>
    </Tab>
    
    {/* Share with Users Tab */}
    <Tab label="Share with Users">
      <UserSearch
        placeholder="Search users by email..."
        onSelect={addSharedUser}
      />
      
      <SharedUsersList>
        {sharedUsers.map(user => (
          <SharedUserItem
            user={user}
            permissions={user.permissions}
            onChangePermissions={updateUserPermissions}
            onRemove={removeSharedUser}
          />
        ))}
      </SharedUsersList>
    </Tab>
    
    {/* Embed Code Tab */}
    <Tab label="Embed">
      <CodeBlock
        language="html"
        code={generateEmbedCode(selectedFile)}
        copyable
      />
      
      <EmbedPreview>
        <iframe src={selectedFile.cdn_url} />
      </EmbedPreview>
    </Tab>
  </TabsContainer>
</ShareDialog>
```

═══════════════════════════════════════════════════════════════════
## 🔍 FILE PREVIEW MODAL
═══════════════════════════════════════════════════════════════════

```tsx
<PreviewModal file={previewFile} open={previewOpen} onClose={closePreview}>
  {/* Universal Previewer */}
  {file.file_type === FileType.IMAGE && (
    <ImagePreview
      src={file.cdn_url}
      alt={file.original_filename}
      zoom={true}
      rotate={true}
      download={true}
    />
  )}
  
  {file.file_type === FileType.VIDEO && (
    <VideoPlayer
      src={file.cdn_url}
      controls={true}
      autoplay={false}
      poster={file.thumbnail_url}
    />
  )}
  
  {file.file_type === FileType.AUDIO && (
    <AudioPlayer
      src={file.cdn_url}
      waveform={true}
      playlist={false}
    />
  )}
  
  {file.file_type === FileType.DOCUMENT && file.mime_type === "application/pdf" && (
    <PDFViewer
      src={file.cdn_url}
      page={currentPage}
      onPageChange={setCurrentPage}
      zoom={zoom}
      search={true}
    />
  )}
  
  {file.file_type === FileType.CODE && (
    <CodeEditor
      value={fileContent}
      language={detectLanguage(file.original_filename)}
      readOnly={true}
      theme="vs-dark"
      lineNumbers={true}
    />
  )}
  
  {/* Preview Actions */}
  <PreviewActions>
    <Button onClick={downloadFile}>Download</Button>
    <Button onClick={shareFile}>Share</Button>
    <Button onClick={addToCollection}>Add to Collection</Button>
  </PreviewActions>
</PreviewModal>
```

═══════════════════════════════════════════════════════════════════
## 📊 STORAGE ANALYTICS (`/storage/analytics`)
═══════════════════════════════════════════════════════════════════

```tsx
<StorageAnalytics>
  <StatsGrid>
    <StatCard
      title="Total Storage"
      value="2.3 GB"
      subtitle="of 10 GB"
      percentage={23}
      trend="+12% this month"
    />
    <StatCard
      title="Files"
      value="1,234"
      subtitle="across all folders"
      icon={<FileIcon />}
    />
    <StatCard
      title="Downloads"
      value="5,678"
      subtitle="this month"
      trend="+23%"
    />
    <StatCard
      title="Bandwidth"
      value="45.6 GB"
      subtitle="transferred"
      trend="+15%"
    />
  </StatsGrid>
  
  <ChartsGrid>
    <StorageUsageChart
      data={storageByType}
      type="pie"
      title="Storage by Type"
    />
    
    <UploadTrendChart
      data={uploadHistory}
      type="line"
      title="Upload Activity"
    />
    
    <TopFilesChart
      data={topFiles}
      type="bar"
      title="Most Downloaded"
    />
  </ChartsGrid>
  
  <FileTypeBreakdown>
    {fileTypeStats.map(stat => (
      <FileTypeStat
        type={stat.type}
        count={stat.count}
        size={stat.size}
        percentage={stat.percentage}
      />
    ))}
  </FileTypeBreakdown>
</StorageAnalytics>
```

═══════════════════════════════════════════════════════════════════
## 🔑 KEY FEATURES
═══════════════════════════════════════════════════════════════════

### **1. Drag & Drop Upload**
- Multi-file upload
- Resume support
- Progress tracking
- Speed & ETA display

### **2. Folder Organization**
- Nested folders (unlimited depth)
- Breadcrumb navigation
- Folder tree sidebar
- Quick folders (Recent, Starred, Shared, Trash)

### **3. File Management**
- Rename, move, copy, delete
- Bulk operations
- Version control
- File recovery (trash)

### **4. Sharing & Permissions**
- Public/private/shared
- Password-protected links
- Expiring links
- Download limits
- User-based sharing

### **5. Search & Filter**
- Full-text search
- Filter by type, date, size
- Tag-based search
- Advanced filters

### **6. Preview**
- Images (zoom, rotate)
- Videos (player)
- Audio (waveform)
- PDFs (viewer)
- Code (syntax highlighting)

### **7. Analytics**
- Storage usage
- Upload/download stats
- Bandwidth tracking
- Popular files

═══════════════════════════════════════════════════════════════════
## 🎨 COMPONENT LIBRARY
═══════════════════════════════════════════════════════════════════

Use shadcn/ui v4 components:
- `Button`, `Input`, `Select`, `Switch`
- `Dialog`, `DropdownMenu`, `ContextMenu`
- `Card`, `Table`, `Tabs`
- `Progress`, `Badge`, `Avatar`
- `Tooltip`, `Popover`, `Sheet`

Custom components:
- `FileCard`, `FolderCard`
- `UploadZone`, `UploadProgress`
- `FilePreview`, `ImageZoom`
- `VideoPlayer`, `AudioPlayer`
- `PDFViewer`, `CodeEditor`
- `ShareDialog`, `PermissionsEditor`
- `StorageUsageBar`, `FileTypeIcon`

═══════════════════════════════════════════════════════════════════
## 🔄 STATE MANAGEMENT
═══════════════════════════════════════════════════════════════════

**Zustand Store:**
```typescript
interface StorageState {
  // Files & Folders
  files: StorageFile[];
  folders: StorageFolder[];
  currentFolder: string | null;
  selectedFiles: string[];
  
  // UI State
  viewMode: "grid" | "list" | "preview";
  sortOrder: string;
  filterType: FileType | null;
  searchQuery: string;
  
  // Upload
  uploads: Upload[];
  uploadQueue: File[];
  
  // Actions
  uploadFiles: (files: File[]) => Promise<void>;
  downloadFile: (fileId: string) => Promise<void>;
  deleteFile: (fileId: string) => Promise<void>;
  shareFile: (fileId: string, options: ShareOptions) => Promise<ShareLink>;
  createFolder: (name: string, parentId?: string) => Promise<StorageFolder>;
  moveFile: (fileId: string, folderId: string) => Promise<void>;
  
  // Selection
  selectFile: (fileId: string) => void;
  clearSelection: () => void;
  selectAll: () => void;
}
```

═══════════════════════════════════════════════════════════════════

**Implementation Priority:**
1. File browser (grid/list view)
2. Upload (drag & drop)
3. Download
4. Folder management
5. Share links
6. Preview
7. Search
8. Analytics
9. Version control
10. Advanced permissions

**Total Implementation Time:** 3-4 weeks for complete storage system

