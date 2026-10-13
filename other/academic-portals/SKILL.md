---
name: academic-portals
description: Access Brazilian academic portals (SIGAA, Moodle, Blackboard) — login, navigate JSF interfaces, download materials, extract files behind jsfcljs() form submissions.
---

# Academic Portals

Accessing academic systems like **SIGAA** (used by UFRN, IFC, IFSC, UFPB, and dozens of Brazilian federal institutions) to download course materials.

## When to Load

- User asks you to enter their SIGAA / academic portal and get content
- User shares login credentials for a portal
- User needs PDFs, slides, or materials from a course page

## General Approach

### 1. Login
- Navigate to the login URL
- Accept any privacy dialogs (clicar "Ciente")
- Fill in usuário and senha fields
- Click "Entrar"

### 2. Navigate to the Course
- Find the course in the "Turmas do Semestre" table
- Click the course name link
- Wait for JSF redirect to the virtual classroom

### 3. Locate Materials
- The page shows course sections organized by "Unidade" (unit)
- Each unit has links to attached files (PDFs, slides)
- Scroll down to see all content

### 4. Download Files

SIGAA provides **two paths** to download files. Use whichever is available.

#### Path A — Principal/Aulas View (hash IDs, form action = `ava/index.jsf`)
- Navigate to the "Principal" tab from the Turma sidebar
- Scroll through the lesson topics (aulas) — each has file links
- Links use hex hash file IDs (e.g., `C85DEA539EC8D648DC2E8EDBB7EF140092A6E674`)
- Extract JSESSIONID and POST the form data (see technique below)

#### Path B — Arquivos Tab (numeric IDs, form action = `ava/ArquivoTurma/listar_discente.jsf`)
- In "Materiais" section, click the "Arquivos" tab
- Shows ALL files in a single table, organized by unit
- Each row has a "Baixar Arquivo" link; component IDs look like `formAva:j_id_jsp_1721837501_309j_id_N`
- File IDs are **numeric** (e.g., `3394591`)
- Has a **"Baixar todos os arquivos"** link to download everything as a single archive
- Download links open in `_blank` — browser tools can't capture them; use the cookie+curl approach

**Do NOT rely on clicking JSF links with `_blank` target** — browser tools can't capture downloads opened in new windows. Instead, extract the JSESSIONID cookie and use `curl` or Python to POST the form data.

## JSF Download Technique (SIGAA)

SIGAA uses Java Server Faces (JSF) with the `jsfcljs()` JavaScript function to serve file downloads.

### Step-by-step

1. **Get the session cookie** from the browser context:
   ```
   browser_console expression="document.cookie"
   ```
   Extract `JSESSIONID=...` and `SERVERID=...` values.

2. **Get the form state**: extract `javax.faces.ViewState` from the page:
   ```python
   import re
   vs = re.search(r'javax\.faces\.ViewState[^>]*value="([^"]+)"', page_text).group(1)
   ```

3. **Identify form parameters** from the link's onclick handler:
   ```javascript
   // Path A (hash IDs, from topic/lesson view):
   jsfcljs(document.getElementById('formAva'), {
     'formAva:...:listaMateriais:N:j_id_jsp_...': 'formAva:...:listaMateriais:N:j_id_jsp_...',
     'id': 'C85DEA539EC8D648DC2E8EDBB7EF140092A6E674'
   }, '_blank');

   // Path B (numeric IDs, from Arquivos tab):
   jsfcljs(document.getElementById('formAva'), {
     'formAva:j_id_jsp_1721837501_309j_id_5': 'formAva:j_id_jsp_1721837501_309j_id_5',
     'id': '3394591'
   }, '_blank');
   ```
   You need:
   - The `button_param` (the long JSF-generated input name used twice as key and value)
   - The `id` (file identifier, hex string or numeric)

4. **Download with curl**:
   ```bash
   data='formAva=formAva&formAva%3AidTopicoSelecionado=0&javax.faces.ViewState=j_id2&{button_param}={button_param}&id={file_id}'

   curl -s -o "FILENAME.pdf" \
     -b "JSESSIONID=XXX; SERVERID=YYY" \
     -X POST -d "$data" \
     "https://sig.ifc.edu.br/sigaa/ava/index.jsf"
   ```

   If using the **Arquivos tab** (Path B), the action URL may differ:
   ```
   "https://sig.ifc.edu.br/sigaa/ava/ArquivoTurma/listar_discente.jsf"
   ```
   Check `document.getElementById('formAva').action` in the browser to confirm.

5. **Or use Python** with `requests`:
   ```python
   import requests
   cookies = {'JSESSIONID': '...', 'SERVERID': '...'}
   data = {
       'formAva': 'formAva',
       'formAva:idTopicoSelecionado': '0',
       'javax.faces.ViewState': 'j_id2',
       button_param: button_param,
       'id': file_id,
   }
   r = requests.post('https://sig.ifc.edu.br/sigaa/ava/index.jsf',
                     data=data, cookies=cookies)
   with open('FILENAME.pdf', 'wb') as f:
       f.write(r.content)
   ```

### Finding All File IDs from the Arquivos Tab

From the browser console, extract all download links at once:
```javascript
var allLinks = document.querySelectorAll('a');
var files = [];
for(var i=0; i<allLinks.length; i++) {
    var onclick = allLinks[i].getAttribute('onclick') || '';
    if(onclick.includes('jsfcljs') && onclick.includes("'id'")) {
        var idMatch = onclick.match(/'id':'(\d+)'/);
        if(idMatch) files.push({id: idMatch[1], onclick: onclick.substring(0,200)});
    }
}
console.table(files);
```

## Pitfalls

- **`_blank` target**: JSF links open downloads in new windows — browser tools can't capture them. Always use the cookie+curl approach.
- **Vision fail**: DeepSeek/open-code-zen doesn't support `image_url` content type. browser_vision will fail. Pivot to browser_console DOM queries instead.
- **JSF ViewState**: May vary between sessions. Always extract the current `javax.faces.ViewState` from the form before constructing your POST.
- **File names with special chars**: Portuguese characters (ã, ç) in filenames can cause WSL/mount issues. Use underscores when saving to `/mnt/c/` paths.
- **Session timeout**: SIGAA sessions have a visible countdown. Refresh the page if downloads start failing with 403/redirect to login.
- **JSF component IDs change between sessions**: The `j_id_jsp_1721837501_309` prefix varies. Always extract fresh IDs from the current page HTML — never hardcode them.
- **Two ID formats**: Hash IDs (40 hex chars, from topic/lesson view) vs numeric IDs (from Arquivos tab). Know which path you're on.
- **Form action URL differs by tab**: Principal/Aulas view uses `ava/index.jsf`; Arquivos tab uses `ava/ArquivoTurma/listar_discente.jsf`. Check `document.getElementById('formAva').action` to confirm.
- **The Arquivos tab download may NOT return PDF directly** — the POST returns HTML (the same page). Use the Principal/Aulas view (Path A) as the primary download path; treat the Arquivos tab (Path B) as a listing/metadata source only.
