---
name: elm-development
description: Comprehensive Elm functional programming for web development including The Elm Architecture, type system, JavaScript interop, and production-ready patterns
---

# Elm Development

A comprehensive skill for building reliable web applications using Elm, a functional programming language that compiles to JavaScript. Elm offers no runtime errors in practice, friendly compiler messages, and a delightful development experience through strong typing and pure functional programming.

## When to Use This Skill

Use this skill when:

- Building web applications that require high reliability and zero runtime errors
- Creating SPAs (Single Page Applications) with predictable state management
- Developing user interfaces with strong type safety guarantees
- Working on projects where refactoring safety is critical
- Building applications with complex state that needs to be managed cleanly
- Creating web apps that benefit from functional programming patterns
- Developing projects where friendly error messages aid rapid development
- Integrating Elm components into existing JavaScript applications
- Building interactive web applications with real-time features
- Creating maintainable, long-lived codebases with clear contracts

## Core Concepts

### The Elm Architecture (TEA)

The Elm Architecture is a pattern for building interactive applications that emerged naturally from Elm development. It inspired Redux and similar state management patterns.

**Core Components:**

1. **Model**: The complete state of your application
2. **View**: A pure function that renders the model as HTML
3. **Update**: A pure function that updates the model based on messages

**Data Flow:**
```
Model → View → HTML
   ↑             ↓
   └── Update ←──┘
        Messages
```

**Basic Pattern:**
```elm
type alias Model =
    { count : Int }

type Msg
    = Increment
    | Decrement

init : Model
init =
    { count = 0 }

update : Msg -> Model -> Model
update msg model =
    case msg of
        Increment ->
            { model | count = model.count + 1 }

        Decrement ->
            { model | count = model.count - 1 }

view : Model -> Html Msg
view model =
    div []
        [ button [ onClick Decrement ] [ text "-" ]
        , div [] [ text (String.fromInt model.count) ]
        , button [ onClick Increment ] [ text "+" ]
        ]
```

### Extended Architecture with Effects

For real applications, you need side effects (HTTP, random, etc.):

**Enhanced Components:**
- **init**: Returns `(Model, Cmd Msg)` - initial state plus commands to run
- **update**: Returns `(Model, Cmd Msg)` - new state plus commands to run
- **subscriptions**: Listens to external events (time, websockets, etc.)
- **view**: Same pure function rendering HTML

**Program Types:**
- `Browser.sandbox`: Simple apps without side effects
- `Browser.element`: Apps with side effects (HTTP, etc.)
- `Browser.document`: Control over `<title>` and `<body>`
- `Browser.application`: Full SPA with URL routing

### Type System Fundamentals

Elm's type system prevents runtime errors through static analysis and type inference.

**Type Annotations:**
```elm
-- Function type annotations
add : Int -> Int -> Int
add x y = x + y

-- Record type alias
type alias User =
    { id : Int
    , name : String
    , email : String
    }

-- Custom types (sum types / tagged unions)
type UserStatus
    = Active
    | Suspended
    | Deleted

-- Parametric types
type Result error value
    = Ok value
    | Err error
```

**Type Inference:**
Elm infers types automatically, but annotations are recommended for top-level functions:

```elm
-- Compiler infers: String -> String
greet name =
    "Hello, " ++ name

-- Better: Add explicit annotation
greet : String -> String
greet name =
    "Hello, " ++ name
```

**Benefits:**
- Catches type errors at compile time
- Provides excellent error messages
- Enables fearless refactoring
- Documents function signatures
- No null/undefined errors

### Maybe and Result Types

Elm eliminates null/undefined errors using Maybe and Result.

**Maybe Type:**
```elm
type Maybe a
    = Just a
    | Nothing

-- Example: Finding a user
findUser : Int -> Maybe User
findUser id =
    -- Returns Just user if found, Nothing otherwise
    ...

-- Pattern matching on Maybe
case findUser 123 of
    Just user ->
        "Found: " ++ user.name

    Nothing ->
        "User not found"

-- Helper functions
Maybe.withDefault : a -> Maybe a -> a
Maybe.map : (a -> b) -> Maybe a -> Maybe b
Maybe.andThen : (a -> Maybe b) -> Maybe a -> Maybe b
```

**Result Type:**
```elm
type Result error value
    = Ok value
    | Err error

-- Example: Validating user input
validateAge : String -> Result String Int
validateAge input =
    case String.toInt input of
        Nothing ->
            Err "Not a valid number"

        Just age ->
            if age < 0 then
                Err "Age cannot be negative"
            else if age > 150 then
                Err "Age seems unrealistic"
            else
                Ok age

-- Using Result
case validateAge "25" of
    Ok age ->
        "Valid age: " ++ String.fromInt age

    Err error ->
        "Error: " ++ error
```

### Pattern Matching

Pattern matching is fundamental to Elm programming:

```elm
-- Matching on custom types
type Traffic
    = Red
    | Yellow
    | Green

describe : Traffic -> String
describe light =
    case light of
        Red ->
            "Stop"
        Yellow ->
            "Prepare to stop"
        Green ->
            "Go"

-- Matching on lists
describeList : List a -> String
describeList list =
    case list of
        [] ->
            "Empty list"

        [single] ->
            "One item"

        [first, second] ->
            "Two items"

        _ ->
            "Many items"

-- Matching with extraction
type User
    = Anonymous
    | LoggedIn String Int

getUserName : User -> String
getUserName user =
    case user of
        Anonymous ->
            "Guest"

        LoggedIn name _ ->
            name
```

## Language Features

### Functions

**Function Definition:**
```elm
-- Simple function
double : Int -> Int
double x =
    x * 2

-- Multiple parameters
add : Int -> Int -> Int
add x y =
    x + y

-- Partial application
add5 : Int -> Int
add5 =
    add 5

-- Anonymous functions (lambdas)
doubleList : List Int -> List Int
doubleList numbers =
    List.map (\n -> n * 2) numbers

-- Pipe operator
result : Int
result =
    [1, 2, 3, 4, 5]
        |> List.map double
        |> List.filter (\n -> n > 5)
        |> List.sum

-- Function composition
addThenDouble : Int -> Int
addThenDouble =
    add 3 >> double
```

**Let Expressions:**
```elm
calculateArea : Float -> Float -> Float
calculateArea width height =
    let
        perimeter =
            2 * (width + height)

        area =
            width * height
    in
    area
```

### Records

**Record Syntax:**
```elm
-- Record type alias
type alias Point =
    { x : Float
    , y : Float
    }

-- Creating records
origin : Point
origin =
    { x = 0, y = 0 }

-- Accessing fields
getX : Point -> Float
getX point =
    point.x

-- Field access function
.x origin  -- Returns 0

-- Updating records (immutable)
moveRight : Point -> Point
moveRight point =
    { point | x = point.x + 1 }

-- Updating multiple fields
moveDiagonal : Point -> Point
moveDiagonal point =
    { point
        | x = point.x + 1
        , y = point.y + 1
    }

-- Pattern matching on records
distance : Point -> Float
distance { x, y } =
    sqrt (x * x + y * y)
```

### Lists and Arrays

**Lists (Linked Lists):**
```elm
-- List literals
numbers : List Int
numbers =
    [1, 2, 3, 4, 5]

-- Cons operator
moreNumbers : List Int
moreNumbers =
    0 :: numbers  -- [0, 1, 2, 3, 4, 5]

-- List functions
List.map : (a -> b) -> List a -> List b
List.filter : (a -> Bool) -> List a -> List a
List.foldl : (a -> b -> b) -> b -> List a -> b
List.length : List a -> Int
List.reverse : List a -> List a
List.sort : List comparable -> List comparable
List.concat : List (List a) -> List a

-- Example usage
processNumbers : List Int -> Int
processNumbers nums =
    nums
        |> List.filter (\n -> n > 0)
        |> List.map (\n -> n * 2)
        |> List.sum
```

**Arrays (Random Access):**
```elm
import Array exposing (Array)

-- Arrays for fast random access
numbers : Array Int
numbers =
    Array.fromList [1, 2, 3, 4, 5]

-- Array operations
Array.get : Int -> Array a -> Maybe a
Array.set : Int -> a -> Array a -> Array a
Array.push : a -> Array a -> Array a
Array.length : Array a -> Int
```

### Modules and Imports

**Module Definition:**
```elm
module Utils exposing (capitalize, truncate)

-- Private function (not exposed)
isBlank : String -> Bool
isBlank str =
    String.trim str == ""

-- Public function
capitalize : String -> String
capitalize str =
    if isBlank str then
        str
    else
        String.toUpper (String.left 1 str) ++ String.dropLeft 1 str

-- Public function
truncate : Int -> String -> String
truncate maxLength str =
    if String.length str > maxLength then
        String.left (maxLength - 3) str ++ "..."
    else
        str
```

**Import Syntax:**
```elm
-- Import entire module
import List
import Dict

-- Import with alias
import Json.Decode as Decode
import Json.Encode as Encode

-- Import specific functions
import List exposing (map, filter, foldl)

-- Import all exposed functions (use sparingly)
import Html exposing (..)
```

## The Elm Architecture in Depth

### Commands (Cmd)

Commands represent side effects to perform:

```elm
type Msg
    = FetchUser
    | GotUser (Result Http.Error User)

init : (Model, Cmd Msg)
init =
    ( { user = Nothing }
    , Cmd.none  -- No command initially
    )

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        FetchUser ->
            ( model
            , Http.get
                { url = "/api/user"
                , expect = Http.expectJson GotUser userDecoder
                }
            )

        GotUser result ->
            case result of
                Ok user ->
                    ( { model | user = Just user }
                    , Cmd.none
                    )

                Err _ ->
                    ( model
                    , Cmd.none
                    )

-- Combining commands
Cmd.batch : List (Cmd msg) -> Cmd msg
Cmd.batch
    [ fetchUser
    , fetchPosts
    , logEvent
    ]
```

### Subscriptions (Sub)

Subscriptions listen to external events:

```elm
import Browser.Events
import Time

type Msg
    = Tick Time.Posix
    | KeyPressed String
    | MouseMoved Int Int

subscriptions : Model -> Sub Msg
subscriptions model =
    if model.isActive then
        Sub.batch
            [ Time.every 1000 Tick
            , Browser.Events.onKeyPress keyDecoder
            , Browser.Events.onMouseMove mouseDecoder
            ]
    else
        Sub.none

-- Subscription functions
Time.every : Float -> (Time.Posix -> msg) -> Sub msg
Browser.Events.onKeyPress : Decode.Decoder msg -> Sub msg
Browser.Events.onAnimationFrame : (Time.Posix -> msg) -> Sub msg
```

### View Functions

**HTML Generation:**
```elm
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

view : Model -> Html Msg
view model =
    div [ class "container" ]
        [ header [ class "header" ]
            [ h1 [] [ text "My App" ]
            ]
        , main_ [ class "content" ]
            [ viewUserForm model.form
            , viewUserList model.users
            ]
        , footer [ class "footer" ]
            [ text "© 2025" ]
            ]

-- Conditional rendering
viewIf : Bool -> Html msg -> Html msg
viewIf condition content =
    if condition then
        content
    else
        text ""

-- List rendering
viewUserList : List User -> Html Msg
viewUserList users =
    div [ class "user-list" ]
        [ h2 [] [ text "Users" ]
        , ul [] (List.map viewUser users)
        ]

viewUser : User -> Html Msg
viewUser user =
    li [ class "user-item" ]
        [ text user.name
        , button [ onClick (DeleteUser user.id) ]
            [ text "Delete" ]
        ]
```

### State Management Patterns

**Nested Updates:**
```elm
type alias Model =
    { loginForm : LoginForm
    , settings : Settings
    }

type Msg
    = LoginFormMsg LoginFormMsg
    | SettingsMsg SettingsMsg

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        LoginFormMsg formMsg ->
            let
                (newForm, formCmd) =
                    LoginForm.update formMsg model.loginForm
            in
            ( { model | loginForm = newForm }
            , Cmd.map LoginFormMsg formCmd
            )

        SettingsMsg settingsMsg ->
            let
                (newSettings, settingsCmd) =
                    Settings.update settingsMsg model.settings
            in
            ( { model | settings = newSettings }
            , Cmd.map SettingsMsg settingsCmd
            )
```

## HTTP and JSON

### Making HTTP Requests

**GET Requests:**
```elm
import Http
import Json.Decode as Decode

type Msg
    = FetchData
    | GotData (Result Http.Error String)

fetchData : Cmd Msg
fetchData =
    Http.get
        { url = "https://api.example.com/data"
        , expect = Http.expectString GotData
        }

-- With JSON decoder
type alias User =
    { id : Int
    , name : String
    }

fetchUser : Int -> Cmd Msg
fetchUser userId =
    Http.get
        { url = "https://api.example.com/users/" ++ String.fromInt userId
        , expect = Http.expectJson GotUser userDecoder
        }

userDecoder : Decode.Decoder User
userDecoder =
    Decode.map2 User
        (Decode.field "id" Decode.int)
        (Decode.field "name" Decode.string)
```

**POST Requests:**
```elm
import Json.Encode as Encode

type Msg
    = CreateUser
    | UserCreated (Result Http.Error User)

createUser : String -> String -> Cmd Msg
createUser name email =
    Http.post
        { url = "https://api.example.com/users"
        , body = Http.jsonBody (encodeUser name email)
        , expect = Http.expectJson UserCreated userDecoder
        }

encodeUser : String -> String -> Encode.Value
encodeUser name email =
    Encode.object
        [ ("name", Encode.string name)
        , ("email", Encode.string email)
        ]
```

**Custom Requests:**
```elm
updateUser : Int -> User -> Cmd Msg
updateUser userId user =
    Http.request
        { method = "PUT"
        , headers = [ Http.header "Authorization" "Bearer token123" ]
        , url = "https://api.example.com/users/" ++ String.fromInt userId
        , body = Http.jsonBody (encodeUserUpdate user)
        , expect = Http.expectJson UserUpdated userDecoder
        , timeout = Just 10000
        , tracker = Nothing
        }
```

### JSON Decoding

**Basic Decoders:**
```elm
import Json.Decode as Decode exposing (Decoder)

-- Primitive decoders
stringDecoder : Decoder String
stringDecoder = Decode.string

intDecoder : Decoder Int
intDecoder = Decode.int

floatDecoder : Decoder Float
floatDecoder = Decode.float

boolDecoder : Decoder Bool
boolDecoder = Decode.bool

-- Field extraction
nameDecoder : Decoder String
nameDecoder =
    Decode.field "name" Decode.string

-- Nested fields
streetDecoder : Decoder String
streetDecoder =
    Decode.at ["address", "street"] Decode.string
```

**Complex Decoders:**
```elm
type alias User =
    { id : Int
    , name : String
    , email : String
    , age : Maybe Int
    , isActive : Bool
    }

userDecoder : Decoder User
userDecoder =
    Decode.map5 User
        (Decode.field "id" Decode.int)
        (Decode.field "name" Decode.string)
        (Decode.field "email" Decode.string)
        (Decode.maybe (Decode.field "age" Decode.int))
        (Decode.field "is_active" Decode.bool)

-- Alternative with pipeline style (requires elm-json-decode-pipeline)
userDecoderPipeline : Decoder User
userDecoderPipeline =
    Decode.succeed User
        |> required "id" Decode.int
        |> required "name" Decode.string
        |> required "email" Decode.string
        |> optional "age" (Decode.maybe Decode.int) Nothing
        |> required "is_active" Decode.bool
```

**List and Array Decoders:**
```elm
-- Decode list of users
usersDecoder : Decoder (List User)
usersDecoder =
    Decode.list userDecoder

-- Decode field containing list
postsDecoder : Decoder (List Post)
postsDecoder =
    Decode.field "posts" (Decode.list postDecoder)

-- Decode dictionary
userByIdDecoder : Decoder (Dict String User)
userByIdDecoder =
    Decode.dict userDecoder
```

**Handling Decode Errors:**
```elm
type Msg
    = GotData (Result Http.Error Data)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        GotData result ->
            case result of
                Ok data ->
                    ( { model | data = Just data }
                    , Cmd.none
                    )

                Err httpError ->
                    case httpError of
                        Http.BadUrl url ->
                            ( { model | error = Just ("Bad URL: " ++ url) }
                            , Cmd.none
                            )

                        Http.Timeout ->
                            ( { model | error = Just "Request timeout" }
                            , Cmd.none
                            )

                        Http.NetworkError ->
                            ( { model | error = Just "Network error" }
                            , Cmd.none
                            )

                        Http.BadStatus code ->
                            ( { model | error = Just ("Bad status: " ++ String.fromInt code) }
                            , Cmd.none
                            )

                        Http.BadBody message ->
                            ( { model | error = Just ("Decode error: " ++ message) }
                            , Cmd.none
                            )
```

## JavaScript Interop

### Flags (Initial Data)

Pass data from JavaScript to Elm on initialization:

**Elm Side:**
```elm
type alias Flags =
    { apiKey : String
    , userId : Int
    , theme : String
    }

init : Flags -> (Model, Cmd Msg)
init flags =
    ( { apiKey = flags.apiKey
      , userId = flags.userId
      , theme = flags.theme
      , data = Nothing
      }
    , fetchUserData flags.userId
    )

main : Program Flags Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }
```

**JavaScript Side:**
```javascript
var app = Elm.Main.init({
    node: document.getElementById('app'),
    flags: {
        apiKey: 'your-api-key',
        userId: 12345,
        theme: 'dark'
    }
});
```

### Ports (Bidirectional Communication)

**Defining Ports:**
```elm
port module Main exposing (..)

-- Port for sending data to JavaScript
port saveToLocalStorage : String -> Cmd msg

-- Port for receiving data from JavaScript
port onStorageChange : (String -> msg) -> Sub msg

-- Using ports in update
type Msg
    = SaveData String
    | StorageChanged String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        SaveData data ->
            ( model
            , saveToLocalStorage data
            )

        StorageChanged data ->
            ( { model | data = data }
            , Cmd.none
            )

-- Using ports in subscriptions
subscriptions : Model -> Sub Msg
subscriptions model =
    onStorageChange StorageChanged
```

**JavaScript Side:**
```javascript
var app = Elm.Main.init({
    node: document.getElementById('app')
});

// Receiving from Elm
app.ports.saveToLocalStorage.subscribe(function(data) {
    localStorage.setItem('app-data', data);
});

// Sending to Elm
window.addEventListener('storage', function(e) {
    if (e.key === 'app-data') {
        app.ports.onStorageChange.send(e.newValue);
    }
});
```

**Common Port Patterns:**
```elm
-- Local storage
port setStorage : String -> Cmd msg
port getStorage : (String -> msg) -> Sub msg

-- WebSocket
port sendSocketMessage : String -> Cmd msg
port receiveSocketMessage : (String -> msg) -> Sub msg

-- Analytics
port trackEvent : { category : String, action : String } -> Cmd msg

-- Third-party libraries
port initMap : { lat : Float, lng : Float } -> Cmd msg
port updateMarker : { lat : Float, lng : Float } -> Cmd msg
```

### Custom Elements

Embed Elm in existing applications using web components:

**JavaScript Side:**
```javascript
customElements.define('elm-widget', class extends HTMLElement {
    connectedCallback() {
        this.app = Elm.Widget.init({
            node: this,
            flags: {
                initialValue: this.getAttribute('value')
            }
        });

        // Listen to Elm events
        this.app.ports.valueChanged.subscribe(value => {
            this.dispatchEvent(new CustomEvent('change', { detail: value }));
        });
    }
});
```

**HTML Usage:**
```html
<elm-widget value="initial"></elm-widget>
```

## Tooling and Build System

### elm.json Configuration

**Package vs Application:**
```json
{
    "type": "application",
    "source-directories": [
        "src"
    ],
    "elm-version": "0.19.1",
    "dependencies": {
        "direct": {
            "elm/browser": "1.0.2",
            "elm/core": "1.0.5",
            "elm/html": "1.0.0",
            "elm/http": "2.0.0",
            "elm/json": "1.1.3"
        },
        "indirect": {}
    },
    "test-dependencies": {
        "direct": {
            "elm-explorations/test": "1.2.2"
        },
        "indirect": {}
    }
}
```

### Common Elm Commands

**Building:**
```bash
# Compile to JavaScript
elm make src/Main.elm --output=main.js

# Compile with optimization
elm make src/Main.elm --output=main.js --optimize

# Compile multiple files
elm make src/Main.elm src/Admin.elm --output=dist/

# Debug build
elm make src/Main.elm --output=main.js --debug
```

**Development:**
```bash
# Start development server
elm reactor

# Install packages
elm install elm/http
elm install elm/json
elm install elm/random

# Format code
elm-format src/ --yes

# Run tests
elm-test
```

**Optimization:**
```bash
# Build optimized
elm make src/Main.elm --output=main.js --optimize

# Minify with uglify-js
uglifyjs main.js --compress 'pure_funcs=[F2,F3,F4,F5,F6,F7,F8,F9,A2,A3,A4,A5,A6,A7,A8,A9],pure_getters,keep_fargs=false,unsafe_comps,unsafe' | uglifyjs --mangle --output main.min.js
```

### Project Structure

**Recommended Structure:**
```
my-elm-app/
├── elm.json                 # Package configuration
├── src/
│   ├── Main.elm            # Entry point
│   ├── Models/
│   │   ├── User.elm
│   │   └── Post.elm
│   ├── Views/
│   │   ├── Home.elm
│   │   ├── Profile.elm
│   │   └── Common/
│   │       ├── Header.elm
│   │       └── Footer.elm
│   ├── Updates/
│   │   ├── User.elm
│   │   └── Post.elm
│   ├── Api/
│   │   ├── User.elm
│   │   └── Post.elm
│   ├── Utils/
│   │   ├── Validators.elm
│   │   └── Formatters.elm
│   └── Ports.elm
├── tests/
│   └── Tests.elm
├── public/
│   ├── index.html
│   ├── styles.css
│   └── assets/
└── README.md
```

## Common Patterns

### Form Handling

**Complete Form Pattern:**
```elm
type alias Form =
    { email : String
    , password : String
    , errors : List String
    , isSubmitting : Bool
    }

type FormMsg
    = UpdateEmail String
    | UpdatePassword String
    | SubmitForm
    | FormSubmitted (Result Http.Error User)

initForm : Form
initForm =
    { email = ""
    , password = ""
    , errors = []
    , isSubmitting = False
    }

updateForm : FormMsg -> Form -> (Form, Cmd FormMsg)
updateForm msg form =
    case msg of
        UpdateEmail email ->
            ( { form | email = email }
            , Cmd.none
            )

        UpdatePassword password ->
            ( { form | password = password }
            , Cmd.none
            )

        SubmitForm ->
            case validateForm form of
                Ok validForm ->
                    ( { form | isSubmitting = True, errors = [] }
                    , submitForm validForm
                    )

                Err errors ->
                    ( { form | errors = errors }
                    , Cmd.none
                    )

        FormSubmitted result ->
            case result of
                Ok user ->
                    ( initForm
                    , Cmd.none
                    )

                Err _ ->
                    ( { form
                        | isSubmitting = False
                        , errors = ["Submission failed"]
                      }
                    , Cmd.none
                    )

validateForm : Form -> Result (List String) Form
validateForm form =
    let
        errors =
            [ validateEmail form.email
            , validatePassword form.password
            ]
            |> List.filterMap identity
    in
    if List.isEmpty errors then
        Ok form
    else
        Err errors

viewForm : Form -> Html FormMsg
viewForm form =
    Html.form [ onSubmit SubmitForm ]
        [ input
            [ type_ "email"
            , value form.email
            , onInput UpdateEmail
            , disabled form.isSubmitting
            ]
            []
        , input
            [ type_ "password"
            , value form.password
            , onInput UpdatePassword
            , disabled form.isSubmitting
            ]
            []
        , div [ class "errors" ]
            (List.map viewError form.errors)
        , button
            [ type_ "submit"
            , disabled form.isSubmitting
            ]
            [ text (if form.isSubmitting then "Submitting..." else "Submit") ]
        ]
```

### Routing (SPA Navigation)

**URL Routing with Browser.application:**
```elm
import Browser
import Browser.Navigation as Nav
import Url
import Url.Parser as Parser exposing (Parser, oneOf, s, int, (</>))

type Route
    = Home
    | Profile Int
    | Settings
    | NotFound

routeParser : Parser (Route -> a) a
routeParser =
    oneOf
        [ Parser.map Home Parser.top
        , Parser.map Profile (s "profile" </> int)
        , Parser.map Settings (s "settings")
        ]

fromUrl : Url.Url -> Route
fromUrl url =
    Parser.parse routeParser url
        |> Maybe.withDefault NotFound

type alias Model =
    { key : Nav.Key
    , route : Route
    }

type Msg
    = LinkClicked Browser.UrlRequest
    | UrlChanged Url.Url

init : () -> Url.Url -> Nav.Key -> (Model, Cmd Msg)
init _ url key =
    ( { key = key
      , route = fromUrl url
      }
    , Cmd.none
    )

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        LinkClicked urlRequest ->
            case urlRequest of
                Browser.Internal url ->
                    ( model
                    , Nav.pushUrl model.key (Url.toString url)
                    )

                Browser.External href ->
                    ( model
                    , Nav.load href
                    )

        UrlChanged url ->
            ( { model | route = fromUrl url }
            , Cmd.none
            )

view : Model -> Browser.Document Msg
view model =
    { title = "My App"
    , body =
        [ viewNavigation
        , viewRoute model.route
        ]
    }

viewRoute : Route -> Html Msg
viewRoute route =
    case route of
        Home ->
            viewHome

        Profile userId ->
            viewProfile userId

        Settings ->
            viewSettings

        NotFound ->
            div [] [ text "404 Not Found" ]

main : Program () Model Msg
main =
    Browser.application
        { init = init
        , view = view
        , update = update
        , subscriptions = \_ -> Sub.none
        , onUrlChange = UrlChanged
        , onUrlRequest = LinkClicked
        }
```

### Debouncing User Input

**Search with Debounce:**
```elm
type alias Model =
    { searchQuery : String
    , searchDebounce : Int
    , results : List Result
    }

type Msg
    = UpdateSearch String
    | DebounceTick Time.Posix
    | PerformSearch
    | GotResults (Result Http.Error (List Result))

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        UpdateSearch query ->
            ( { model
                | searchQuery = query
                , searchDebounce = 3  -- Wait 3 ticks
              }
            , Cmd.none
            )

        DebounceTick _ ->
            if model.searchDebounce > 0 then
                ( { model | searchDebounce = model.searchDebounce - 1 }
                , Cmd.none
                )
            else if model.searchQuery /= "" then
                update PerformSearch model
            else
                ( model, Cmd.none )

        PerformSearch ->
            ( model
            , searchApi model.searchQuery
            )

        GotResults result ->
            case result of
                Ok results ->
                    ( { model | results = results }
                    , Cmd.none
                    )

                Err _ ->
                    ( model, Cmd.none )

subscriptions : Model -> Sub Msg
subscriptions model =
    Time.every 300 DebounceTick  -- Check every 300ms
```

### Loading States

**Remote Data Pattern:**
```elm
type RemoteData error value
    = NotAsked
    | Loading
    | Success value
    | Failure error

type alias Model =
    { userData : RemoteData Http.Error User
    }

type Msg
    = FetchUser
    | GotUser (Result Http.Error User)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        FetchUser ->
            ( { model | userData = Loading }
            , fetchUser
            )

        GotUser result ->
            case result of
                Ok user ->
                    ( { model | userData = Success user }
                    , Cmd.none
                    )

                Err error ->
                    ( { model | userData = Failure error }
                    , Cmd.none
                    )

viewUser : RemoteData Http.Error User -> Html Msg
viewUser userData =
    case userData of
        NotAsked ->
            button [ onClick FetchUser ] [ text "Load User" ]

        Loading ->
            div [ class "spinner" ] [ text "Loading..." ]

        Success user ->
            div [ class "user" ]
                [ h2 [] [ text user.name ]
                , p [] [ text user.email ]
                ]

        Failure error ->
            div [ class "error" ]
                [ text "Failed to load user"
                , button [ onClick FetchUser ] [ text "Retry" ]
                ]
```

## Best Practices

### Code Organization

1. **Keep Modules Small**: Each module should have a single responsibility
2. **Use Type Aliases**: Document complex types with meaningful names
3. **Expose Minimally**: Only expose what's needed from modules
4. **Group Related Code**: Keep related types, functions, and views together
5. **Consistent Naming**: Use clear, consistent naming conventions

### Type Safety

1. **Always Add Type Annotations**: For top-level functions
2. **Use Custom Types**: Instead of strings/ints for states
3. **Make Impossible States Impossible**: Design types to prevent invalid states
4. **Leverage Maybe and Result**: Never use defaults that hide errors
5. **Pattern Match Exhaustively**: Cover all cases explicitly

### Performance

1. **Use Html.Lazy**: For expensive view functions that rarely change
2. **Optimize List Operations**: Consider using Array for random access
3. **Batch Commands**: Use Cmd.batch for multiple effects
4. **Minimize Subscriptions**: Only subscribe when needed
5. **Profile Before Optimizing**: Use elm reactor debugger

### Testing

```elm
import Test exposing (..)
import Expect

suite : Test
suite =
    describe "User Validation"
        [ test "validates correct email" <|
            \_ ->
                validateEmail "test@example.com"
                    |> Expect.equal (Ok "test@example.com")

        , test "rejects invalid email" <|
            \_ ->
                validateEmail "invalid"
                    |> Expect.err

        , describe "Password validation"
            [ test "requires minimum length" <|
                \_ ->
                    validatePassword "short"
                        |> Expect.err

            , test "accepts valid password" <|
                \_ ->
                    validatePassword "securePassword123"
                        |> Expect.ok
            ]
        ]
```

### Error Handling

1. **Use Result for Validation**: Return meaningful error messages
2. **Handle All Http.Error Cases**: Provide user-friendly messages
3. **Display Errors Clearly**: Show validation errors next to form fields
4. **Provide Recovery Options**: Offer retry buttons, alternative actions
5. **Log Errors via Ports**: Send to external logging services

### Accessibility

```elm
-- Use semantic HTML
viewButton : String -> msg -> Html msg
viewButton label msg =
    button
        [ onClick msg
        , ariaLabel label
        ]
        [ text label ]

-- Provide keyboard navigation
viewModal : Html msg
viewModal =
    div
        [ role "dialog"
        , ariaModal True
        , tabindex -1
        ]
        [ -- modal content
        ]

-- Use ARIA attributes
viewStatus : String -> Html msg
viewStatus message =
    div
        [ ariaLive "polite"
        , ariaAtomic True
        ]
        [ text message ]
```

## Resources and Learning

**Official Resources:**
- Elm Guide: https://guide.elm-lang.org
- Package Documentation: https://package.elm-lang.org
- Elm Discourse: https://discourse.elm-lang.org
- Elm Slack: https://elmlang.herokuapp.com

**Key Packages:**
- elm/browser - Browser-based programs
- elm/html - HTML generation
- elm/http - HTTP requests
- elm/json - JSON encoding/decoding
- elm/random - Random value generation
- elm/time - Time and dates
- elm/url - URL parsing and building
- elm-explorations/test - Testing framework

**Learning Resources:**
- Elm in Action (book)
- Elm Radio (podcast)
- Elm Weekly (newsletter)
- Exercism Elm Track

---

**Skill Version**: 1.0.0
**Last Updated**: November 2025
**Skill Category**: Functional Programming, Web Development, Type-Safe Programming
**Compatible With**: JavaScript, Web Components, SPA Frameworks
