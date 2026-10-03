---
name: liveview-component
invocable: true
description: >
  Tworzenie komponentów LiveView w projekcie DriverHub.
  Użyj dla formularzy, list, tabel z danymi czasu rzeczywistego.
---

# LiveView Component — Przewodnik

## Placeholdery

W szablonach używaj:
- `<AppName>` → nazwa aplikacji (np. `DriverHub`)
- `<AppNameWeb>` → moduł web (np. `DriverHubWeb`)
- `<Domain>` → domena Ash (np. `Drivers`, `Companies`, `Orders`)
- `<Resource>` → nazwa resource (np. `Driver`, `Company`, `Order`)
- `<resource>` → nazwa w lowercase (np. `driver`, `company`, `order`)
- `<resources>` → liczba mnoga (np. `drivers`, `companies`, `orders`)

## Konwencje

- Komponenty LiveView w `lib/<app_name>_web/live/`
- Używaj `AshPhoenix.Form` do formularzy Ash
- Tailwind CSS do stylowania
- Streamy do list z dużą ilością danych
- Composable components w `lib/<app_name>_web/components/`

## Struktura plików

```
lib/<app_name>_web/
├── live/
│   ├── <resources>_live/
│   │   ├── index.ex          # Lista
│   │   ├── show.ex           # Szczegóły
│   │   └── form_component.ex # Formularz (modal)
│   └── ...
└── components/
    ├── core_components.ex    # Podstawowe komponenty Phoenix
    └── ui_components.ex      # Własne komponenty UI
```

## Routing

W `lib/<app_name>_web/router.ex`:

```elixir
scope "/", <AppNameWeb> do
  pipe_through :browser

  live "/<resources>", <Resource>sLive.Index, :index
  live "/<resources>/new", <Resource>sLive.Index, :new
  live "/<resources>/:id", <Resource>sLive.Show, :show
  live "/<resources>/:id/edit", <Resource>sLive.Show, :edit
end
```

## Szablon LiveView - Lista z Stream

```elixir
defmodule <AppNameWeb>.<Resource>sLive.Index do
  use <AppNameWeb>, :live_view

  alias <AppName>.<Domain>.<Resource>

  @impl true
  def mount(_params, _session, socket) do
    <resources> = Ash.read!(<Resource>)

    {:ok,
     socket
     |> assign(:page_title, "<Resources>")
     |> stream(:<resources>, <resources>)}
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
  end

  defp apply_action(socket, :index, _params) do
    assign(socket, :<resource>, nil)
  end

  defp apply_action(socket, :new, _params) do
    assign(socket, :<resource>, %<Resource>{})
  end

  @impl true
  def handle_info({:<resource>_saved, <resource>}, socket) do
    {:noreply, stream_insert(socket, :<resources>, <resource>)}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    <resource> = Ash.get!(<Resource>, id)
    Ash.destroy!(<resource>)

    {:noreply, stream_delete(socket, :<resources>, <resource>)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="max-w-4xl mx-auto p-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold"><Resources></h1>
        <.link patch={~p"/<resources>/new"} class="btn-primary">
          Dodaj
        </.link>
      </div>

      <div id="<resources>" phx-update="stream" class="grid gap-4">
        <.<resource>_card :for={{dom_id, <resource>} <- @streams.<resources>} id={dom_id} <resource>={<resource>} />
      </div>

      <.modal :if={@live_action in [:new, :edit]} id="<resource>-modal" show on_cancel={JS.patch(~p"/<resources>")}>
        <.live_component
          module={<AppNameWeb>.<Resource>sLive.FormComponent}
          id={@<resource>.id || :new}
          action={@live_action}
          <resource>={@<resource>}
          patch={~p"/<resources>"}
        />
      </.modal>
    </div>
    """
  end

  defp <resource>_card(assigns) do
    ~H"""
    <div id={@id} class="border rounded-lg p-4 flex justify-between items-center">
      <div>
        <p class="font-semibold"><%= @<resource>.name %></p>
        <%!-- Dodatkowe pola --%>
      </div>
      <div class="flex gap-2">
        <.link patch={~p"/<resources>/#{@<resource>}/edit"} class="text-blue-600 hover:underline">
          Edytuj
        </.link>
        <button phx-click="delete" phx-value-id={@<resource>.id} data-confirm="Na pewno usunąć?">
          Usuń
        </button>
      </div>
    </div>
    """
  end
end
```

## Formularz z AshPhoenix.Form

```elixir
defmodule <AppNameWeb>.<Resource>sLive.FormComponent do
  use <AppNameWeb>, :live_component

  alias <AppName>.<Domain>.<Resource>

  @impl true
  def update(%{<resource>: <resource>, action: action} = assigns, socket) do
    form =
      if action == :new do
        AshPhoenix.Form.for_create(<Resource>, :create, as: "<resource>")
      else
        AshPhoenix.Form.for_update(<resource>, :update, as: "<resource>")
      end

    {:ok,
     socket
     |> assign(assigns)
     |> assign(:form, to_form(form))}
  end

  @impl true
  def handle_event("validate", %{"<resource>" => params}, socket) do
    form = AshPhoenix.Form.validate(socket.assigns.form.source, params)
    {:noreply, assign(socket, :form, to_form(form))}
  end

  @impl true
  def handle_event("save", %{"<resource>" => params}, socket) do
    case AshPhoenix.Form.submit(socket.assigns.form.source, params: params) do
      {:ok, <resource>} ->
        send(self(), {:<resource>_saved, <resource>})

        {:noreply,
         socket
         |> put_flash(:info, "Zapisano")
         |> push_patch(to: socket.assigns.patch)}

      {:error, form} ->
        {:noreply, assign(socket, :form, to_form(form))}
    end
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <h2 class="text-xl font-bold mb-4">
        <%= if @action == :new, do: "Nowy", else: "Edytuj" %>
      </h2>

      <.form for={@form} phx-target={@myself} phx-change="validate" phx-submit="save">
        <div class="space-y-4">
          <div>
            <.input field={@form[:name]} label="Nazwa" />
          </div>

          <%!-- Dodatkowe pola formularza --%>

          <div class="flex justify-end gap-2 pt-4">
            <.link patch={@patch} class="btn-secondary">Anuluj</.link>
            <.button type="submit" phx-disable-with="Zapisuję...">Zapisz</.button>
          </div>
        </div>
      </.form>
    </div>
    """
  end
end
```

## Widok szczegółów (Show)

```elixir
defmodule <AppNameWeb>.<Resource>sLive.Show do
  use <AppNameWeb>, :live_view

  alias <AppName>.<Domain>.<Resource>

  @impl true
  def mount(%{"id" => id}, _session, socket) do
    <resource> = Ash.get!(<Resource>, id)

    {:ok,
     socket
     |> assign(:page_title, <resource>.name)
     |> assign(:<resource>, <resource>)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="max-w-2xl mx-auto p-6">
      <.link navigate={~p"/<resources>"} class="text-blue-600 hover:underline mb-4 block">
        ← Powrót do listy
      </.link>

      <div class="bg-white shadow rounded-lg p-6">
        <h1 class="text-2xl font-bold mb-4"><%= @<resource>.name %></h1>

        <dl class="grid grid-cols-2 gap-4">
          <%!-- Pola do wyświetlenia --%>
        </dl>
      </div>
    </div>
    """
  end
end
```

## Typowe handle_event

```elixir
# Toggle boolean
def handle_event("toggle_active", %{"id" => id}, socket) do
  <resource> = Ash.get!(<Resource>, id)
  {:ok, updated} = Ash.update(<resource>, %{active: !<resource>.active}, action: :update)
  {:noreply, stream_insert(socket, :<resources>, updated)}
end

# Filtrowanie
def handle_event("filter", %{"status" => status}, socket) do
  <resources> = Ash.read!(<Resource>, query: [filter: [status: status]])
  {:noreply, stream(socket, :<resources>, <resources>, reset: true)}
end

# Sortowanie
def handle_event("sort", %{"field" => field}, socket) do
  <resources> = Ash.read!(<Resource>, query: [sort: [{String.to_atom(field), :asc}]])
  {:noreply, stream(socket, :<resources>, <resources>, reset: true)}
end

# Live search
def handle_event("search", %{"query" => query}, socket) do
  <resources> = Ash.read!(<Resource>, query: [filter: [name: [contains: query]]])
  {:noreply, stream(socket, :<resources>, <resources>, reset: true)}
end
```

## Komponenty funkcyjne

W `lib/<app_name>_web/components/ui_components.ex`:

```elixir
defmodule <AppNameWeb>.UIComponents do
  use Phoenix.Component

  attr :status, :atom, required: true
  def status_badge(assigns) do
    ~H"""
    <span class={[
      "px-2 py-1 rounded-full text-xs font-medium",
      status_color(@status)
    ]}>
      <%= status_label(@status) %>
    </span>
    """
  end

  defp status_color(:active), do: "bg-green-100 text-green-800"
  defp status_color(:pending), do: "bg-yellow-100 text-yellow-800"
  defp status_color(:inactive), do: "bg-red-100 text-red-800"
  defp status_color(_), do: "bg-gray-100 text-gray-800"

  defp status_label(:active), do: "Aktywny"
  defp status_label(:pending), do: "Oczekujący"
  defp status_label(:inactive), do: "Nieaktywny"
  defp status_label(status), do: status

  attr :label, :string, required: true
  attr :value, :string, required: true
  def info_row(assigns) do
    ~H"""
    <div class="flex justify-between py-2 border-b">
      <span class="text-gray-500"><%= @label %></span>
      <span class="font-medium"><%= @value %></span>
    </div>
    """
  end

  attr :empty_message, :string, default: "Brak danych"
  slot :inner_block, required: true
  def empty_state(assigns) do
    ~H"""
    <div class="text-center py-12 text-gray-500">
      <p><%= @empty_message %></p>
      <%= render_slot(@inner_block) %>
    </div>
    """
  end
end
```

## Tailwind - przydatne klasy

```elixir
# Przyciski
"bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"  # Primary
"border border-gray-300 px-4 py-2 rounded hover:bg-gray-50"   # Secondary
"text-red-600 hover:text-red-800"                              # Danger link

# Karty
"bg-white shadow rounded-lg p-6"

# Formularze
"w-full border rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"

# Grid responsywny
"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
```

## Przykład użycia - Driver

Zamień placeholdery:
- `<AppName>` → `DriverHub`
- `<AppNameWeb>` → `DriverHubWeb`
- `<Domain>` → `Drivers`
- `<Resource>` → `Driver`
- `<resource>` → `driver`
- `<resources>` → `drivers`
- `<Resources>` → `Kierowcy`

## Zasady

- Używaj `stream/3` dla list (nie `assign` dla kolekcji)
- Zawsze `phx-update="stream"` na kontenerze listy
- Formularze przez `AshPhoenix.Form` (nie ręczne changesety)
- `live_component` dla formularzy w modalach
- `handle_info` do komunikacji między komponentami
- Walidacja przez `phx-change="validate"`
