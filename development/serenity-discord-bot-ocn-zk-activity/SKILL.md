---
name: serenity-discord-bot
description: Discord bot development with Serenity 0.11. Covers event handlers, slash commands, embeds, interactions, TypeMapKey for shared state, and message sending patterns. Use when creating Discord commands, building embeds, handling interactions, or working with the Discord API.
---

# Serenity Discord Bot Guidelines

## Purpose

Development patterns for Discord bots using Serenity 0.11, specifically tailored to this project's architecture.

## When to Use

- Creating or modifying slash commands
- Building Discord embeds
- Handling Discord events
- Working with interactions
- Sending messages to channels
- Managing bot state

---

## Project Architecture

### Key Files

```
src/
  discord_bot.rs   # EventHandler, message sending, embed building
  commands.rs      # Command trait, helper functions
  commands/
    subscribe.rs   # /subscribe command
    unsubscribe.rs # /unsubscribe command
    diag.rs        # /diag command
    ...
```

### State Management

The bot uses `TypeMapKey` to store shared state in Serenity's context:

```rust
// In lib.rs
pub struct AppStateContainer;
impl TypeMapKey for AppStateContainer {
    type Value = Arc<AppState>;
}

pub struct CommandMap;
impl TypeMapKey for CommandMap {
    type Value = Arc<HashMap<String, Box<dyn Command>>>;
}

// Usage in handlers
let data = ctx.data.read().await;
let app_state = data.get::<AppStateContainer>().unwrap();
```

---

## Event Handler

### Basic Structure

```rust
use serenity::async_trait;
use serenity::prelude::*;
use serenity::model::gateway::Ready;
use serenity::model::prelude::Interaction;

pub struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn ready(&self, ctx: Context, data_about_bot: Ready) {
        info!("Discord bot {} is connected!", data_about_bot.user.name);
        // Register commands here
    }

    async fn interaction_create(&self, ctx: Context, interaction: Interaction) {
        match interaction {
            Interaction::ApplicationCommand(command) => {
                // Handle slash commands
            }
            Interaction::MessageComponent(component) => {
                // Handle button clicks, select menus
            }
            _ => {}
        }
    }
}
```

### Registering Global Commands

```rust
async fn ready(&self, ctx: Context, _: Ready) {
    let data = ctx.data.read().await;
    let command_map = data.get::<CommandMap>().unwrap();

    serenity::model::application::command::Command::set_global_application_commands(
        &ctx.http,
        |commands| {
            for cmd in command_map.values() {
                commands.create_application_command(|c| cmd.register(c));
            }
            commands
        },
    ).await.expect("Failed to register commands");
}
```

---

## Slash Commands

### Command Trait Pattern

```rust
use serenity::async_trait;
use serenity::builder::CreateApplicationCommand;
use serenity::model::prelude::interaction::application_command::ApplicationCommandInteraction;

#[async_trait]
pub trait Command: Send + Sync {
    fn name(&self) -> String;

    fn register<'a>(
        &self,
        command: &'a mut CreateApplicationCommand,
    ) -> &'a mut CreateApplicationCommand;

    async fn execute(
        &self,
        ctx: &Context,
        command: &ApplicationCommandInteraction,
        app_state: &Arc<AppState>,
    );
}
```

### Implementing a Command

```rust
pub struct MyCommand;

#[async_trait]
impl Command for MyCommand {
    fn name(&self) -> String {
        "mycommand".to_string()
    }

    fn register<'a>(
        &self,
        command: &'a mut CreateApplicationCommand,
    ) -> &'a mut CreateApplicationCommand {
        command
            .name("mycommand")
            .description("Description of my command")
            .create_option(|opt| {
                opt.name("required_arg")
                    .description("A required argument")
                    .kind(CommandOptionType::String)
                    .required(true)
            })
            .create_option(|opt| {
                opt.name("optional_arg")
                    .description("An optional argument")
                    .kind(CommandOptionType::Integer)
                    .required(false)
            })
    }

    async fn execute(
        &self,
        ctx: &Context,
        command: &ApplicationCommandInteraction,
        app_state: &Arc<AppState>,
    ) {
        // Extract options
        let required = get_option_value(&command.data.options, "required_arg")
            .and_then(|v| match v {
                CommandDataOptionValue::String(s) => Some(s.clone()),
                _ => None,
            });

        // Respond
        command.create_interaction_response(&ctx.http, |r| {
            r.interaction_response_data(|m| m.content("Response!"))
        }).await.unwrap();
    }
}
```

### Helper for Extracting Options

```rust
pub fn get_option_value<'a>(
    options: &'a [CommandDataOption],
    name: &str,
) -> Option<&'a CommandDataOptionValue> {
    options
        .iter()
        .find(|opt| opt.name == name)
        .and_then(|opt| opt.resolved.as_ref())
}
```

---

## Building Embeds

### Basic Embed

```rust
use serenity::builder::CreateEmbed;
use serenity::utils::Colour;

let mut embed = CreateEmbed::default();
embed.title("Embed Title");
embed.url("https://example.com");
embed.description("Embed description text");
embed.color(Colour::DARK_GREEN);
embed.thumbnail("https://example.com/image.png");
embed.footer(|f| f.text("Footer text"));
embed.timestamp(chrono::Utc::now().to_rfc3339());
```

### Embed with Fields

```rust
embed.field("Field Name", "Field value", false);  // false = not inline
embed.field("Inline 1", "Value", true);
embed.field("Inline 2", "Value", true);
```

### Embed with Author

```rust
embed.author(|a| {
    a.name("Author Name")
     .url("https://author.link")
     .icon_url("https://icon.url")
});
```

### This Project's Embed Pattern

```rust
async fn build_killmail_embed(
    app_state: &Arc<AppState>,
    zk_data: &ZkData,
) -> CreateEmbed {
    let mut embed = CreateEmbed::default();

    // Build dynamically based on data
    embed.title(format!("`{}` destroyed", victim_ship_name));
    embed.url(format!("https://zkillboard.com/kill/{}/", kill_id));
    embed.author(|a| {
        a.name(author_text)
         .url(related_br_url)
         .icon_url(alliance_icon_url)
    });
    embed.thumbnail(ship_icon_url);
    embed.color(Colour::DARK_GREEN);
    embed.field("Attackers", attacker_info, false);
    embed.footer(|f| f.text(format!("Value: {}", value_str)));

    embed
}
```

---

## Sending Messages

### To a Channel

```rust
use serenity::model::prelude::ChannelId;

let channel = ChannelId(channel_id_u64);

channel.send_message(&ctx.http, |m| {
    m.content("Message content")
     .set_embed(embed)
}).await?;
```

### With Optional Ping

```rust
channel.send_message(http, |m| {
    if should_ping {
        m.content("@everyone")
    } else {
        m
    }
    .set_embed(embed)
}).await?;
```

### Responding to Interactions

```rust
// Initial response
command.create_interaction_response(&ctx.http, |r| {
    r.interaction_response_data(|m| {
        m.content("Processing...")
         .ephemeral(true)  // Only visible to user
    })
}).await?;

// Follow-up (can be used multiple times)
command.create_followup_message(&ctx.http, |m| {
    m.content("Follow-up message")
}).await?;

// Edit original response
command.edit_original_interaction_response(&ctx.http, |m| {
    m.content("Updated response")
}).await?;
```

---

## Error Handling for Discord Operations

### Pattern for Message Sending

```rust
pub enum KillmailSendError {
    CleanupChannel(serenity::Error),  // Channel deleted/no access
    Other(Box<dyn std::error::Error + Send + Sync>),
}

pub async fn send_message(/* ... */) -> Result<(), KillmailSendError> {
    let result = channel.send_message(http, |m| m.set_embed(embed)).await;

    if let Err(e) = result {
        if let serenity::Error::Http(http_err) = &e {
            match &**http_err {
                Error::UnsuccessfulRequest(resp) => match resp.status_code {
                    StatusCode::FORBIDDEN => {
                        // Bot removed or no permission
                        return Err(KillmailSendError::CleanupChannel(e));
                    }
                    StatusCode::NOT_FOUND => {
                        // Channel deleted
                        return Err(KillmailSendError::CleanupChannel(e));
                    }
                    _ => {}
                },
                _ => {}
            }
        }
        return Err(KillmailSendError::Other(Box::new(e)));
    }
    Ok(())
}
```

---

## Component Interactions (Buttons, Select Menus)

### Creating a Select Menu

```rust
command.create_interaction_response(&ctx.http, |r| {
    r.interaction_response_data(|m| {
        m.content("Select an option:")
         .components(|c| {
             c.create_action_row(|row| {
                 row.create_select_menu(|menu| {
                     menu.custom_id("my_select_menu")
                        .placeholder("Choose...")
                        .options(|opts| {
                            opts.create_option(|o| {
                                o.label("Option 1")
                                 .value("opt1")
                                 .description("Description")
                            })
                        })
                 })
             })
         })
    })
}).await?;
```

### Handling Component Interaction

```rust
Interaction::MessageComponent(component) => {
    let custom_id = &component.data.custom_id;

    if custom_id.starts_with("my_select_menu") {
        let selected = &component.data.values;
        // Handle selection...

        component.create_interaction_response(&ctx.http, |r| {
            r.interaction_response_data(|m| {
                m.content("Selection received!")
                 .ephemeral(true)
            })
        }).await?;
    }
}
```

---

## GatewayIntents

```rust
let intents = GatewayIntents::non_privileged()
    | GatewayIntents::GUILDS
    | GatewayIntents::GUILD_MESSAGES
    | GatewayIntents::DIRECT_MESSAGES
    | GatewayIntents::MESSAGE_CONTENT  // Privileged!
    | GatewayIntents::GUILD_INTEGRATIONS;

let mut client = Client::builder(&token, intents)
    .event_handler(Handler)
    .await?;
```

---

## Quick Reference

| Task | Method |
|------|--------|
| Get shared state | `ctx.data.read().await.get::<T>()` |
| Send to channel | `ChannelId(id).send_message(&http, \|m\| ...)` |
| Reply to command | `command.create_interaction_response(...)` |
| Build embed | `CreateEmbed::default()` then chain methods |
| Make ephemeral | `.ephemeral(true)` in response data |

---

## Reference Files

- [resources/embed-examples.md](resources/embed-examples.md) - Full embed examples
- [resources/command-options.md](resources/command-options.md) - All option types