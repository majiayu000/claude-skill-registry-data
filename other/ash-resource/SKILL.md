---
name: ash-resource
description: >
  Tworzenie i edycja Ash Framework Resources w projekcie DriverHub.
  Uzyj gdy zadanie dotyczy modeli danych, resources, actions lub policies.
user-invocable: true
---

# Ash Resource - Przewodnik

## Generowanie nowego Resource

Zawsze uzywaj Igniter/Ash generatora:

```bash
mix ash.gen.resource DriverHub.<Domain>.<Resource> --extend postgres
mix ash.gen.domain DriverHub.<Domain>
```

Przyklad:
```bash
mix ash.gen.resource DriverHub.Drivers.Driver --extend postgres
mix ash.gen.resource DriverHub.Companies.Company --extend postgres
mix ash.gen.resource DriverHub.Orders.Order --extend postgres
```

## Szablon Resource

```elixir
defmodule DriverHub.<Domain>.<Resource> do
  use Ash.Resource,
    domain: DriverHub.<Domain>,
    data_layer: AshPostgres.DataLayer

  postgres do
    table "<table_name>"
    repo DriverHub.Repo
  end

  attributes do
    uuid_primary_key :id

    # Atrybuty - dostosuj do resource
    attribute :name, :string, allow_nil?: false
    attribute :status, :atom, constraints: [one_of: [:active, :inactive]], default: :active

    timestamps()
  end

  relationships do
    # belongs_to - resource nalezy do innego
    # belongs_to :company, DriverHub.Companies.Company

    # has_many - resource ma wiele innych
    # has_many :orders, DriverHub.Orders.Order
  end

  actions do
    defaults [:read, :destroy]

    create :create do
      accept [:name, :status]
    end

    update :update do
      accept [:name, :status]
    end
  end

  policies do
    # Odczyt - dostepny dla wszystkich
    policy action_type(:read) do
      authorize_if always()
    end

    # Modyfikacje - wymagaja zalogowanego uzytkownika
    policy action_type([:create, :update, :destroy]) do
      authorize_if actor_present()
    end
  end

  identities do
    # Unikalne pola - dostosuj do resource
    # identity :unique_email, [:email]
  end
end
```

## Typowe atrybuty

```elixir
# Tekst
attribute :name, :string, allow_nil?: false
attribute :description, :string

# Email z walidacja
attribute :email, :string, allow_nil?: false

# Enum/Atom z ograniczeniami
attribute :status, :atom, constraints: [one_of: [:pending, :active, :completed]]

# Boolean z domyslna wartoscia
attribute :active, :boolean, default: true

# Liczby
attribute :amount, :decimal
attribute :quantity, :integer

# Data/Czas
attribute :scheduled_at, :utc_datetime

# Array
attribute :tags, {:array, :string}, default: []

# Timestamps (automatyczne)
timestamps()
```

## Typowe relacje

```elixir
relationships do
  # Kierowca nalezy do firmy
  belongs_to :company, DriverHub.Companies.Company

  # Firma ma wielu kierowcow
  has_many :drivers, DriverHub.Drivers.Driver

  # Zlecenie ma jednego kierowce i jedna firme
  belongs_to :driver, DriverHub.Drivers.Driver
  belongs_to :company, DriverHub.Companies.Company
end
```

## Zasady

- Generuj resource przez `mix ash.gen.resource` (Igniter)
- Zawsze definiuj explicit actions (nie uzywaj `defaults [:create, :update]`)
- `uuid_primary_key` zamiast integer ID
- Kazdy resource MUSI miec sekcje `policies`
- Nazwy tabel w liczbie mnogiej: `drivers`, `companies`, `orders`

## Generowanie migracji

Po utworzeniu/edycji resource:

```bash
mix ash.codegen --name nazwa_migracji
mix ash.migrate
```

## Domeny projektu DriverHub

- `DriverHub.Drivers` - kierowcy (Driver)
- `DriverHub.Companies` - firmy przewozowe (Company)
- `DriverHub.Orders` - zlecenia transportowe (Order)
