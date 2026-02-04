---
name: team-management-ux
description: Team invitation and role management UX patterns for SaaS. Covers invitation flows, role assignment, and permissions UI.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason
---

# Team Management UX Skill

## When to Use This Skill

Use this skill when:

- **Team Management Ux tasks** - Working on team invitation and role management ux patterns for saas. covers invitation flows, role assignment, and permissions ui
- **Planning or design** - Need guidance on Team Management Ux approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for team invitation, role management, and permissions UI in multi-tenant SaaS applications.

Team management is a core SaaS workflow. Good team UX reduces friction in adoption, enables self-service administration, and ensures proper access control. This skill covers invitation flows, role assignment, and permissions UI.

## Team Structure Models

```text
+------------------------------------------------------------------+
|                    Team Structure Options                         |
+------------------------------------------------------------------+
| Model          | Structure                | Use Case              |
+----------------+--------------------------+-----------------------+
| Flat           | All users in tenant      | Small teams, simple   |
| Teams          | Tenant → Teams → Users   | Departments, projects |
| Workspaces     | Tenant → Workspaces      | Multiple products     |
| Hierarchical   | Org → Teams → Sub-teams  | Enterprise            |
+----------------+--------------------------+-----------------------+
```

## Invitation Flow

### Invitation States

```text
+------------------------------------------------------------------+
|                    Invitation Flow                                |
+------------------------------------------------------------------+
|                                                                   |
|  +---------+    +----------+    +----------+    +----------+      |
|  | Created |-->| Sent     |-->| Accepted |-->| Active   |       |
|  +---------+    +----------+    +----------+    +----------+      |
|                      |                                            |
|                      v                                            |
|                +----------+                                       |
|                | Expired  |                                       |
|                +----------+                                       |
|                      |                                            |
|                      v                                            |
|                +----------+                                       |
|                | Resent   |--> (back to Sent)                    |
|                +----------+                                       |
|                                                                   |
+------------------------------------------------------------------+
```

### Invitation Service

```csharp
public sealed class InvitationService(
    IDbContext db,
    IEmailService email,
    ITenantContext tenant)
{
    public async Task<Invitation> InviteAsync(
        string emailAddress,
        string role,
        Guid? teamId,
        CancellationToken ct)
    {
        // Check if user already exists
        var existingUser = await db.Users
            .FirstOrDefaultAsync(u => u.Email == emailAddress, ct);

        if (existingUser != null)
        {
            // Add to team directly if user exists
            return await AddExistingUserAsync(existingUser, role, teamId, ct);
        }

        // Create invitation
        var invitation = new Invitation
        {
            Id = Guid.NewGuid(),
            TenantId = tenant.TenantId,
            Email = emailAddress,
            Role = role,
            TeamId = teamId,
            Token = GenerateSecureToken(),
            ExpiresAt = DateTimeOffset.UtcNow.AddDays(7),
            Status = InvitationStatus.Pending,
            InvitedBy = tenant.UserId,
            CreatedAt = DateTimeOffset.UtcNow
        };

        db.Invitations.Add(invitation);
        await db.SaveChangesAsync(ct);

        // Send invitation email
        await email.SendTemplateAsync(emailAddress, "team_invitation", new
        {
            tenant.TenantName,
            InviterName = tenant.UserName,
            Role = role,
            AcceptUrl = $"https://app.example.com/accept-invite?token={invitation.Token}"
        }, ct);

        return invitation;
    }

    public async Task<AcceptResult> AcceptInvitationAsync(
        string token,
        string name,
        string password,
        CancellationToken ct)
    {
        var invitation = await db.Invitations
            .FirstOrDefaultAsync(i => i.Token == token, ct);

        if (invitation == null)
            return AcceptResult.InvalidToken();

        if (invitation.ExpiresAt < DateTimeOffset.UtcNow)
            return AcceptResult.Expired();

        if (invitation.Status != InvitationStatus.Pending)
            return AcceptResult.AlreadyUsed();

        // Create user
        var user = new User
        {
            Id = Guid.NewGuid(),
            TenantId = invitation.TenantId,
            Email = invitation.Email,
            Name = name,
            Role = invitation.Role,
            TeamId = invitation.TeamId,
            PasswordHash = HashPassword(password),
            CreatedAt = DateTimeOffset.UtcNow
        };

        db.Users.Add(user);

        invitation.Status = InvitationStatus.Accepted;
        invitation.AcceptedAt = DateTimeOffset.UtcNow;

        await db.SaveChangesAsync(ct);

        return AcceptResult.Success(user);
    }
}
```

## Role Management

### Role Definitions

```csharp
public static class Roles
{
    public const string Owner = "owner";
    public const string Admin = "admin";
    public const string Member = "member";
    public const string Viewer = "viewer";
    public const string Guest = "guest";

    public static readonly RoleDefinition[] All =
    [
        new(Owner, "Owner", "Full control including billing and deletion", 100),
        new(Admin, "Admin", "Manage team members and settings", 80),
        new(Member, "Member", "Create and edit content", 60),
        new(Viewer, "Viewer", "View content only", 40),
        new(Guest, "Guest", "Limited access to shared items", 20)
    ];

    public static bool CanAssign(string assignerRole, string targetRole)
    {
        var assigner = All.First(r => r.Name == assignerRole);
        var target = All.First(r => r.Name == targetRole);
        return assigner.Level > target.Level;
    }
}

public sealed record RoleDefinition(
    string Name,
    string DisplayName,
    string Description,
    int Level);
```

### Role Assignment API

```csharp
[ApiController]
[Route("api/team")]
public class TeamController : ControllerBase
{
    [HttpPost("members/{userId}/role")]
    [Authorize(Roles = "owner,admin")]
    public async Task<ActionResult> ChangeRole(
        Guid userId,
        [FromBody] ChangeRoleRequest request,
        CancellationToken ct)
    {
        var currentUser = await GetCurrentUserAsync(ct);

        // Validate role assignment permission
        if (!Roles.CanAssign(currentUser.Role, request.NewRole))
        {
            return Forbid("Cannot assign a role equal to or higher than your own");
        }

        // Prevent demoting yourself
        if (userId == currentUser.Id && request.NewRole != currentUser.Role)
        {
            return BadRequest("Cannot change your own role");
        }

        // Ensure at least one owner remains
        if (await IsLastOwnerAsync(userId, ct) && request.NewRole != Roles.Owner)
        {
            return BadRequest("Cannot remove the last owner");
        }

        await _teamService.ChangeRoleAsync(userId, request.NewRole, ct);

        return Ok();
    }
}
```

## Permissions UI

### Permissions Matrix

```text
Permissions Display:
+------------------------------------------------------------------+
|                  Role Permissions Matrix                          |
+------------------------------------------------------------------+
| Permission           | Owner | Admin | Member | Viewer | Guest   |
+----------------------+-------+-------+--------+--------+---------+
| Manage billing       | ✓     | -     | -      | -      | -       |
| Delete tenant        | ✓     | -     | -      | -      | -       |
| Manage team          | ✓     | ✓     | -      | -      | -       |
| Manage settings      | ✓     | ✓     | -      | -      | -       |
| Create projects      | ✓     | ✓     | ✓      | -      | -       |
| Edit projects        | ✓     | ✓     | ✓      | -      | -       |
| View projects        | ✓     | ✓     | ✓      | ✓      | Limited |
| Export data          | ✓     | ✓     | ✓      | -      | -       |
+----------------------+-------+-------+--------+--------+---------+
```

### Permission Checks

```csharp
public sealed class PermissionService(ITenantContext tenant)
{
    private static readonly Dictionary<string, HashSet<string>> RolePermissions = new()
    {
        [Roles.Owner] = ["billing.*", "tenant.*", "team.*", "settings.*", "projects.*", "export"],
        [Roles.Admin] = ["team.invite", "team.remove", "settings.*", "projects.*", "export"],
        [Roles.Member] = ["projects.create", "projects.edit", "projects.view", "export"],
        [Roles.Viewer] = ["projects.view"],
        [Roles.Guest] = ["projects.view:shared"]
    };

    public bool HasPermission(string permission)
    {
        var userRole = tenant.CurrentUser?.Role ?? Roles.Guest;

        if (!RolePermissions.TryGetValue(userRole, out var permissions))
            return false;

        return permissions.Any(p =>
            p == permission ||
            p.EndsWith(".*") && permission.StartsWith(p.Replace(".*", "")));
    }

    public void RequirePermission(string permission)
    {
        if (!HasPermission(permission))
            throw new ForbiddenException($"Permission required: {permission}");
    }
}
```

## Team Settings UI

### Settings Components

```typescript
// Team members list component
interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: string;
  avatarUrl: string;
  joinedAt: string;
  lastActiveAt: string;
}

const TeamMembersList: React.FC<{ members: TeamMember[] }> = ({ members }) => {
  const { currentUser } = useAuth();
  const canManageTeam = ['owner', 'admin'].includes(currentUser.role);

  return (
    <div className="team-members">
      <header>
        <h2>Team Members ({members.length})</h2>
        {canManageTeam && (
          <button onClick={openInviteModal}>Invite Member</button>
        )}
      </header>

      <table>
        <thead>
          <tr>
            <th>Member</th>
            <th>Role</th>
            <th>Joined</th>
            <th>Last Active</th>
            {canManageTeam && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {members.map(member => (
            <TeamMemberRow
              key={member.id}
              member={member}
              canManage={canManageTeam && member.id !== currentUser.id}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### Invitation Modal

```typescript
const InviteModal: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const [emails, setEmails] = useState('');
  const [role, setRole] = useState('member');
  const [sending, setSending] = useState(false);

  const handleInvite = async () => {
    setSending(true);
    const emailList = emails.split(/[,\n]/).map(e => e.trim()).filter(Boolean);

    await Promise.all(emailList.map(email =>
      api.inviteTeamMember({ email, role })
    ));

    setSending(false);
    onClose();
  };

  return (
    <Modal title="Invite Team Members" onClose={onClose}>
      <form onSubmit={handleInvite}>
        <label>
          Email Addresses
          <textarea
            placeholder="Enter emails separated by commas or new lines"
            value={emails}
            onChange={e => setEmails(e.target.value)}
          />
        </label>

        <label>
          Role
          <select value={role} onChange={e => setRole(e.target.value)}>
            <option value="admin">Admin - Full access</option>
            <option value="member">Member - Can create and edit</option>
            <option value="viewer">Viewer - Read-only access</option>
          </select>
        </label>

        <button type="submit" disabled={sending}>
          {sending ? 'Sending...' : 'Send Invitations'}
        </button>
      </form>
    </Modal>
  );
};
```

## Best Practices

```text
Team Management Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Bulk invitation support     | Faster team onboarding             |
| Role preview before assign  | Fewer mistakes                     |
| Invitation expiration       | Security, housekeeping             |
| Audit trail for changes     | Compliance, debugging              |
| Self-service role requests  | Reduced admin burden               |
| Clear permission display    | User understands access            |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| No invitation expiry | Security risk | 7-day expiration |
| Single owner allowed | Bus factor | Allow multiple owners |
| Immediate role changes | Accidental changes | Confirmation dialog |
| No audit trail | Can't debug access | Log all changes |
| Complex role hierarchy | Confusion | Keep roles simple |

## Related Skills

- `self-service-onboarding` - New user onboarding
- `settings-hierarchy` - Team-level settings
- `subscription-models` - Seat-based pricing

## MCP Research

For current patterns:

```text
perplexity: "SaaS team management UX 2024" "invitation flow best practices"
```
