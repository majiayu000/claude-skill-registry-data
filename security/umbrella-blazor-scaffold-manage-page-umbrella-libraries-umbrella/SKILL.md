---
name: umbrella-blazor-scaffold-manage-page
description: 'Scaffold a Blazor manage page (.razor + .razor.cs) for create/edit operations, following the Umbrella EditForm pattern with UmbrellaModelLayoutStateView, breadcrumb, auth policy, and concurrency handling.'
---

# Scaffold Blazor Manage Page

## Purpose

Add a Blazor manage page that handles both create and edit for a feature. The page uses `EditForm` with `UmbrellaModelLayoutStateView` to manage loading states, and dispatches to `Repository.CreateAsync` or `Repository.UpdateAsync` based on whether an ID parameter is present.

**Prerequisite:** A client data service interface (`I<Name>Service`) must exist with `CreateAsync` and `UpdateAsync` methods (i.e. the service interface extends `IGenericDataService` with non-NoOp create/update model types). The concrete create and update models must exist and derive from a shared `CreateUpdate<Name>ModelBase` used by the combined form.

## Discovery (read these before writing anything)

1. Read 2–3 existing manage pages under `Web\<AppName>.Web.Client\Pages\Admin\` to understand the form field patterns, file upload handling if applicable, and navigation after save.
2. Confirm the project-specific client component base class name (e.g. `IndyRecordsClientComponentBase`). `Mapper` (`IUmbrellaMapper`) is a `protected` property on `UmbrellaComponentBase` (the Umbrella framework base) — it is available in all Blazor components in the hierarchy without any injection.
3. Read `Web\<AppName>.Web.Shared\Security\Policies\<AppName>PolicyNames.cs` or `SharedPolicyNames.cs` for the correct auth policy constant.
4. Read the create/update model hierarchy for the feature to know which properties to include as form fields and identify the exact shared create/update base name. Use their exact discovered names and follow the repository's convention (for example, `CreateUpdateManageIndustryModelBase`); do not introduce an input interface as a substitute. If the base is missing, use `umbrella-dotnet-scaffold-api-server-models` to add the shared model hierarchy first.
5. Check `Web\<AppName>.Web.Client.Data\Mappings\Api\` for an existing `<Name>Mapper.cs`. You will need client-side mappers for: `IUmbrellaMapperlyNewInstanceMapper<<Name>Model, Update<Name>Model>` (to populate the edit form) and `IUmbrellaMapperlyExistingInstanceMapper<Update<Name>ResultModel, Update<Name>Model>` (to refresh the concurrency stamp after save). If they do not exist, use the `umbrella-dotnet-scaffold-mapperly-factories` skill to create them first.

---

## Step 1 -- Create Manage.razor

**File:** `Web\<AppName>.Web.Client\Pages\Admin\<Name>Management\Manage.razor`

```razor
@inherits ManageBase
@page "/admin/<route-plural>/manage"
@page "/admin/<route-plural>/manage/{Id:int}"

@{
    string title = "Manage <Names>";
    string subTitle = Id.HasValue ? "Edit" : "Create";
}

<<AppName>PageTitle>@title</<AppName>PageTitle>

<UmbrellaBreadcrumb>
    <UmbrellaBreadcrumbItem Name="@title" Url="/admin/<route-plural>" />
    <UmbrellaBreadcrumbItem Name="@subTitle" />
</UmbrellaBreadcrumb>

<div class="management-page">
    <h1>@title</h1>
    <h4>@subTitle</h4>
    <hr />
    <section>
        <UmbrellaModelLayoutStateView CurrentState="CurrentState" Model="CreateUpdateModel" ReloadCallback="ReloadAsync">
            <Success>
                <UmbrellaValidationSummary ValidationResults="ValidationResults" />
                <EditForm Model="CreateUpdateModel" OnValidSubmit="SubmitFormAsync" novalidate>
                    <ObjectGraphDataAnnotationsValidator />

                    <div class="form-group form-floating">
                        <UmbrellaInputText class="form-control" @bind-Value="CreateUpdateModel!.Name" />
                        <LabelText ForTarget="() => CreateUpdateModel!.Name" />
                        <ValidationMessage For="() => CreateUpdateModel.Name" />
                    </div>

                    <div class="form-group form-group--buttons">
                        <button type="submit" class="btn btn-primary">@(Id.HasValue ? "Save Changes" : "Create <Name>")</button>
                        <a href="/admin/<route-plural>" class="btn btn-secondary">Cancel</a>
                    </div>
                </EditForm>
            </Success>
        </UmbrellaModelLayoutStateView>
    </section>
</div>
```

**Rules:**
- Two `@page` directives: the create route (no ID) and the edit route (`{Id:int}`).
- `@inherits ManageBase` only — no C# logic in the `.razor` beyond the `@{...}` title block.
- `UmbrellaModelLayoutStateView` wraps the form — always present; it handles the loading/error/success state machine.
- `CurrentState` and `ReloadCallback` come from the base class — do not define them.
- Form fields: add one `<div class="form-group">` per genuinely user-editable property. Use `form-floating` for text inputs. Check existing manage pages for the right component per field type (`UmbrellaInputText`, `UmbrellaInputTextArea`, `UmbrellaInputSelect`, etc.). A file-provider filename is not a raw text field: either implement the complete upload/preview workflow below or omit it from this page and explicitly report that file editing is out of scope.
- Cancel button always links back to the index route.
- Submit button label changes based on `Id.HasValue`.

### File upload field pattern

When the feature includes image/file upload:

```razor
<div class="form-group">
    <LabelText ForTarget="() => CreateUpdateModel.<FilePropertyName>" />
    <UmbrellaFileImagePreviewUpload @ref="ImagePreviewUpload"
                                    OnRequestUpload="UploadFileToTempDirectoryAsync"
                                    OnDeleteImage="OnDeleteImage"
                                    Accept="@GlobalFileSystemConstants.<Name>FileExtensions"
                                    MaxFileSizeBytes="@GlobalFileSystemConstants.<Name>MaxSizeBytes"
                                    WidthRequest="400"
                                    HeightRequest="400"
                                    Url="@Model?.ImageUrl"
                                    VersionToken="@Model?.ImageVersionToken" />
    <ValidationMessage For="() => CreateUpdateModel.<FilePropertyName>" />
</div>
```

---

## Step 2 -- Create Manage.razor.cs

**File:** `Web\<AppName>.Web.Client\Pages\Admin\<Name>Management\Manage.razor.cs`

```csharp
using <AppName>.Web.Client.Data.Services.Abstractions;
using <AppName>.Web.Shared.Models.Api.<Feature>;

namespace <AppName>.Web.Client.Pages.Admin.<Name>Management;

[Authorize(<AppName>PolicyNames.<Policy>)]
public abstract class ManageBase : <AppName>ClientComponentBase
{
    [Parameter]
    public int? Id { get; set; }

    [Inject]
    private I<Name>Service Repository { get; set; } = null!;

    protected <Name>Model? Model { get; private set; }
    protected CreateUpdate<Name>ModelBase? CreateUpdateModel { get; private set; }

    protected IReadOnlyCollection<ValidationResult>? ValidationResults { get; private set; }

    protected override async Task OnInitializedAsync()
    {
        try
        {
            if (!Id.HasValue)
            {
                CreateUpdateModel = new Create<Name>Model();
                CurrentState = LayoutState.Success;

                return;
            }

            var result = await Repository.FindByIdAsync(Id.Value);

            if (result.IsSuccess && result.Result is not null)
            {
                Model = result.Result;
                CreateUpdateModel = await Mapper.MapAsync<<Name>Model, Update<Name>Model>(result.Result);

                CurrentState = LayoutState.Success;

                return;
            }
            else
            {
                await ShowOperationResultErrorMessageAsync(result);
            }
        }
        catch (Exception exc) when (Logger.WriteError(exc, new { Id }))
        {
            await DialogUtility.ShowDangerMessageAsync();
        }

        CurrentState = LayoutState.Error;
    }

    protected async Task SubmitFormAsync()
    {
        try
        {
            if (CreateUpdateModel is null)
                throw new InvalidOperationException("The CU model is null");

            if (Id.HasValue && Model is null)
                throw new InvalidOperationException("The model is null");

            if (CreateUpdateModel is Create<Name>Model createModel)
            {
                var result = await Repository.CreateAsync(createModel);

                if (result.IsSuccess)
                {
                    await DialogUtility.ShowSuccessMessageAsync("The <Name> has been created successfully.");
                    Navigation.NavigateTo("/admin/<route-plural>");
                }
                else
                {
                    await ShowOperationResultErrorMessageAsync(result);
                }
            }
            else if (CreateUpdateModel is Update<Name>Model updateModel)
            {
                var result = await Repository.UpdateAsync(updateModel);

                if (result.IsSuccess && result.Result is not null)
                {
                    await DialogUtility.ShowSuccessMessageAsync("The <Name> has been updated successfully.");

                    // Preferred: map the update result back onto the existing model to refresh the
                    // concurrency stamp and any server-computed fields — avoids a full page reload.
                    // Requires IUmbrellaMapperlyExistingInstanceMapper<Update<Name>ResultModel, Update<Name>Model>
                    // in Client.Data. If that mapper does not exist yet, use ReloadAsync() as a fallback.
                    _ = await Mapper.MapAsync(result.Result, updateModel);

                    // Fallback (use when the client-side result mapper has not been created yet):
                    // await ReloadAsync();
                }
                else
                {
                    await ShowOperationResultErrorMessageAsync(result);
                }
            }
        }
        catch (UmbrellaConcurrencyException)
        {
            await DialogUtility.ShowDangerMessageAsync(ClientErrorMessages.Concurrency);
        }
        catch (Exception exc) when (Logger.WriteError(exc, new { Model, CreateUpdateModel }))
        {
            await DialogUtility.ShowDangerMessageAsync();
        }
    }
}
```

**Rules:**
- `public abstract class` — the `.razor` file inherits from it via `@inherits`.
- `[Authorize(PolicyName)]` on the class, not in the `.razor` file.
- `[Inject] private I<Name>Service Repository { get; set; } = null!;` — the property is always named `Repository` by convention, regardless of the type name.
- `CreateUpdateModel` is typed as the exact discovered shared create/update base (illustrated as `CreateUpdate<Name>ModelBase?`), so both sealed concrete create and update models can be assigned without duplicating their shared property contract.
- `OnInitializedAsync`: if no `Id`, construct an empty `Create<Name>Model` and set `CurrentState = LayoutState.Success`. If `Id` is set, load from `Repository.FindByIdAsync` and use `await Mapper.MapAsync<<Name>Model, Update<Name>Model>(result.Result)` to populate `CreateUpdateModel`.
- `SubmitFormAsync`: pattern-match on `CreateUpdateModel` type to call the correct method. After a successful create, navigate to the index route. After a successful update, prefer `_ = await Mapper.MapAsync(result.Result, updateModel)` to refresh the concurrency stamp in place — this requires `IUmbrellaMapperlyExistingInstanceMapper<Update<Name>ResultModel, Update<Name>Model>` in `Client.Data`. If that mapper does not exist yet, fall back to `await ReloadAsync()` and leave a `// TODO: Mapper` comment.
- `Mapper` is a `protected` property on `UmbrellaComponentBase` (the Umbrella framework base) — no injection needed in derived components. The `Mapper.MapAsync` calls require client-side mapper classes in `Web.Client.Data\Mappings\Api\`: `IUmbrellaMapperlyNewInstanceMapper<<Name>Model, Update<Name>Model>` for load, and `IUmbrellaMapperlyExistingInstanceMapper<Update<Name>ResultModel, Update<Name>Model>` for post-save refresh. Use the `umbrella-dotnet-scaffold-mapperly-factories` skill to create them.
- Concurrency exception is caught specifically with a dedicated user message.
- `System.ComponentModel.DataAnnotations` is needed if `ValidationResult` is referenced — add the `using` if required.

### Additional injections for file upload

When file upload is needed, add:

```csharp
[Inject]
private IFileUploadService FileUploadService { get; set; } = null!;

protected UmbrellaFileImagePreviewUpload ImagePreviewUpload { get; set; } = null!;

public async Task<IOperationResult?> UploadFileToTempDirectoryAsync(UmbrellaFileUploadRequestEventArgs evt)
{
    try
    {
        if (CreateUpdateModel is null)
            throw new InvalidOperationException("The model should not be null here.");

        var fileUploadResult = await FileUploadService.UploadAsync(evt.Content, evt.FileName, FileUploadType.<Name>Image, evt.Type, CancellationToken);

        if (fileUploadResult.IsSuccess)
        {
            CreateUpdateModel.<FilePropertyName> = fileUploadResult.Result.tempFileName;

            // Updating the filename alone is not enough on an edit: the server uses this flag
            // to delete the old stored file and promote the new temporary upload.
            if (CreateUpdateModel is Update<Name>Model updateModel)
                updateModel.ReplaceExistingImage = true;

            // Temporary/no-store uploads normally have no token. If the upload contract returns one,
            // pass it as the second argument so the preview emits the fingerprint directly.
            ImagePreviewUpload.Update(fileUploadResult.Result.url);
        }

        StateHasChanged();

        return fileUploadResult;
    }
    catch (Exception exc) when (Logger.WriteError(exc))
    {
        await DialogUtility.ShowDangerMessageAsync();
    }

    return null;
}

protected void OnDeleteImage()
{
    if (CreateUpdateModel is null)
        throw new InvalidOperationException("The model should not be null here.");

    if (CreateUpdateModel is Update<Name>Model updateModel)
        updateModel.ReplaceExistingImage = true;
}
```

---

## Verification

1. Two `@page` directives — create route (no ID) and edit route (`{Id:int}`).
2. `[Authorize(PolicyName)]` is on the code-behind class, not in the `.razor` file.
3. `[Inject]` property is named `Repository` and typed as the service interface.
4. `CreateUpdateModel` is typed as the shared create/update model base (`CreateUpdate<Name>ModelBase?`), not an input interface or one concrete request type.
5. `OnInitializedAsync` uses `await Mapper.MapAsync<<Name>Model, Update<Name>Model>(result.Result)` to populate the edit form — no manual property assignment.
6. `OnInitializedAsync` sets `CurrentState = LayoutState.Success` on both the create and edit success paths, and `LayoutState.Error` on failure.
7. `SubmitFormAsync` pattern-matches on `Create<Name>Model` vs `Update<Name>Model` — navigates after create; after update calls `_ = await Mapper.MapAsync(result.Result, updateModel)` to refresh the model in place.
8. `UmbrellaConcurrencyException` is caught and handled with `ClientErrorMessages.Concurrency`.
9. `UmbrellaModelLayoutStateView` wraps the form content in the `.razor`.
10. Client-side mapper classes exist in `Web.Client.Data\Mappings\Api\` for the `<Name>Model → Update<Name>Model` and `Update<Name>ResultModel → Update<Name>Model` mappings.
11. When the displayed file uses Dynamic Image URL fingerprinting, its model declares `ImageVersionToken`, mappings assign URL/token together, and `UmbrellaFileImagePreviewUpload` receives and forwards `VersionToken`.
12. A successful upload while editing sets the matching replacement flag (`ReplaceExistingImage`, `ReplaceExistingFile`, or the feature-specific equivalent) after assigning the temporary provider filename. Do not rely only on the delete/replace button handler; image-preview upload controls can upload directly over an existing preview.
13. Read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build with the installed analyzers enabled.
