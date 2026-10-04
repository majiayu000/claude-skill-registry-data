---
name: Intraweb Framework
description: Guides and standards for using the Intraweb stateful web framework in Delphi projects.
---

# Intraweb Framework - Spec-Kit

Intraweb is a VCL-for-the-Web framework that allows you to create stateful business web applications in a semantic way similar to creating Desktop applications. When dealing with Intraweb in Copilot or your project, consider the following best practices to ensure maintainability and scalability.

## 1. Sessions (UserSession) and Global Variables
**Golden Rule:** Do not use classic unit `var` global variables or Singleton instances for user data, since Intraweb applications run in a Multithread environment with concurrent sessions (each user has their own).
- To maintain user-specific data, strictly use the `UserSessionUnit.pas` unit (`ServerController.UserSession` Instance).

```pascal
//❌ BAD: Incorrect Usage (Global scope variable serves all sessions, Multithreading problem)
var
  LCustomerId: Integer;

//✅ GOOD: Correct Usage (Safe properties of the current context)
UserSession.CustomerId := 10;
```

## 2. ServerController and Configuration
The global system parameters, database connection pool and initializations that do not depend on the user must be resolved in the `ServerController` (`IWServerController.pas`) object. Avoid injecting heavy dependencies and direct database scopes in `TIWAppForm`.

## 3. Non-Blocking User Interfaces (Asynchronous Callbacks)
In the web context, you should not use blocking code to "wait" for the user, such as `ShowMessage`, `InputBox`, or classic VCL ModalResults calls that rely on code locking on the same line.
- Use the `OnAsyncClick` property for DOM updates without full-screen postback.
- In Intraweb version 15 or newer, explore the capabilities of `WebApplication.ShowMessage` combined with Ajax calls and safe web interface interrupts.

```pascal
//❌ BAD: Blocking the thread on the Intraweb
procedure TIWForm1.iwBtnSaveClick(Sender: TObject);
begin
  if Application.MessageBox('Deseja salvar?', 'Confirme', MB_YESNO) = IDYES then
    //Rescue code
end;

//✅ GOOD: Using Ajax Async from Intraweb
procedure TIWForm1.iwBtnSaveAsyncClick(Sender: TObject; EventParams: TStringList);
begin
  WebApplication.ShowMessage('Registro Salvo via Callback Assíncrono!', smAlert);
end;
```

## 4. Separation of Rules and UI
It is easy to build monstrous projects on the Intraweb by grouping the entire system rule behind the click (ex: num `iwBtnProcessarAsyncClick`). Follow the SRP (Single Responsibility Principle) principles:
- The form maps to the Controller request and re-renders components. The rules remain in the *Application/Services* layer.
- An Application/Service or Repository layer that is used in the Intraweb **cannot couple or know** the `IWApplication` unit (do not use `WebApplication.ShowMessage` among persistence Services).

## 5. Naming of Visual Components (Intraweb Prefixes)
Use `iw` concatenated with the native typologies:
- `TIWButton` -> `iwBtnSave`
- `TIWEdit` -> `iwEdtName`
- `TIWLabel` -> `iwLblTitle`
- `TIWComboBox` -> `iwCmbStatus`
- `TIWGrid` -> `iwGrdItems`
- `TIWRegion` -> `iwRegContainer`

## 6. Dynamic HTML and Custom CSS
Despite being VCL-like, the massive stylizations in the components create large DOMS in the interface. Prefer to define external CSS files using `ExtraHeader` injection in the form and apply the `Css` property to the tags of the T visual components `TIW*` instead of manually painting the color of buttons and fonts via the Object Inspector.
