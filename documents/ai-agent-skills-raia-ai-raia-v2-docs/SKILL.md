# Escalation Skill

## 🆘 Escalation Skill

The **Escalation Skill** ensures that critical user requests are addressed quickly and accurately by enabling seamless escalation from AI to human support.\
By monitoring conversations for predefined keywords or triggers, the system automatically notifies the right people via **email**, **SMS**, **webhook**, or **in-app alerts**.

***

### 💡 Purpose

Escalation bridges the gap between automation and human intervention — ensuring urgent or sensitive requests are handled by the appropriate team members.\
This reduces response delays, improves customer satisfaction, and safeguards against missed opportunities in critical interactions.

***

### ⚙️ How It Works

1. **Monitoring Conversations**\
   The AI watches for escalation keywords or conditions (e.g., “urgent,” “cancel account,” “medical emergency”).
2. **Triggering Escalation**\
   When triggered, the skill automatically sends a message to your designated recipients.
3. **Human Takeover**\
   Optionally, the assistant can switch to _manual conversation mode_ so a live agent can step in immediately.

***

### 🧱 Configuration Steps

1. Click **Add Escalation** in your Escalation Skill settings.
2. Fill in the following fields:

| Field                             | Description                                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Escalation Topic**              | A clear title for the escalation scenario (e.g., “Billing Urgent,” “Medical Priority”).                |
| **Escalation Prompt**             | The internal note sent to your team. Describe what triggered the escalation and what needs to be done. |
| **Auto Change Conversation Mode** | Enable if you want the AI to automatically switch to manual assistant mode during escalation.          |
| **Response Prompt**               | The public message your assistant will send to the user after escalation is triggered.                 |
| **Recipients**                    | Choose how alerts are sent (Email, SMS, Webhook) and add recipient contact info.                       |

***

### 📨 Example Configuration

| Setting                           | Example Value                                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Escalation Topic**              | _Critical Billing Issue_                                                                                |
| **Escalation Prompt**             | “A customer has reported a double charge. Please review the account immediately.”                       |
| **Auto Change Conversation Mode** | ✅ Enabled                                                                                               |
| **Response Prompt**               | “Thanks for letting us know, I’ve alerted our billing team, and a specialist will contact you shortly.” |
| **Recipient**                     | (Email)                                                                                                 |

***

### 📸 Interface Previews

#### Escalation Dashboard

\
Shows the overview of configured escalation topics and their statuses.

<figure><img src="../.gitbook/assets/image (2).png" alt="" width="414"><figcaption></figcaption></figure>

#### Creating an Escalation

\
Displays the configuration panel with topic, prompts, auto-switch toggle, and recipient setup.

<figure><img src="../.gitbook/assets/image (3).png" alt="" width="563"><figcaption></figcaption></figure>

***

### &#x20;Best Practices

* Keep escalation prompts **specific** and **actionable**.
* Use **auto mode** when a human agent needs to take over immediately.
* Regularly **test** your escalation flow to ensure alerts reach the correct team.
* Add **multiple recipients** for critical issues to prevent single-point failure.

***
