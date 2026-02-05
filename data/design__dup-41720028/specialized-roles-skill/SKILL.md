---
name: specialized-roles-skill
description: Master specialized tech careers including Product Management, Engineering Management, DevRel, Technical Writing, QA, Blockchain, Game Development, Cybersecurity, and UX Design. Navigate multiple career paths beyond traditional software development.
---

# Specialized Roles & Tools Skill

Complete guide to career paths beyond traditional software engineering.

## Quick Start

### Choose Your Specialization

```
Product Manager ──────→ Product Strategy
Engineering Manager ──→ Technical Leadership
DevRel ────────────────→ Community & Advocacy
Technical Writer ──────→ Documentation
QA Engineer ───────────→ Quality & Testing
Blockchain Developer ──→ Web3 & Crypto
Game Developer ────────→ Game Engines
Cybersecurity ─────────→ Penetration Testing
```

---

## Product Management

### **Core Responsibilities**

1. **Product Vision & Strategy**
   - Define product roadmap (12-24 months)
   - Set OKRs (Objectives & Key Results)
   - Competitive analysis
   - Market opportunity assessment

2. **Discovery & Requirements**
   ```
   User Research → Feature Prioritization → Specification
        ↓                ↓                        ↓
     Interviews     Importance/Effort    User Stories
     Surveys       Impact Matrix        PRDs (Product Requirement Docs)
   ```

3. **Metrics & Analytics**
   - Define success metrics (KPIs)
   - Track key metrics
   - Analyze user behavior
   - Data-driven decisions

   **Key Metrics Examples:**
   ```
   DAU (Daily Active Users)
   WAU (Weekly Active Users)
   Retention Rate = Users on Day 30 / Users on Day 1
   Churn Rate = 1 - Retention
   LTV (Lifetime Value) = Average revenue per user
   CAC (Customer Acquisition Cost)
   ```

4. **Cross-functional Leadership**
   - Work with engineers, designers, sales, marketing
   - Communicate vision clearly
   - Manage stakeholder expectations
   - Resolve conflicts

### **Product Manager Roadmap**

**Year 1:**
- Master product thinking
- Learn metrics and data analysis
- Build first roadmap
- Launch 2-3 features

**Year 2+:**
- Own product P&L
- Build and mentor team
- Strategic partnerships
- Company-wide influence

### **Tools**
- Figma/Miro (wireframing)
- Jira (project tracking)
- Amplitude/Mixpanel (analytics)
- Notion (documentation)

---

## Engineering Management

### **Core Responsibilities**

1. **Team Leadership**
   - Hire and onboard engineers
   - Conduct 1-on-1 meetings
   - Performance management
   - Career development

2. **Technical Oversight**
   - Architecture decisions
   - Code review standards
   - Technology choices
   - Technical debt management

3. **Delivery & Planning**
   - Sprint planning
   - Risk assessment
   - Timeline estimation
   - Release management

4. **Communication**
   - Team standup facilitation
   - Retrospectives
   - Executive updates
   - Cross-team collaboration

### **Engineering Manager Skills**

```
Technical Skills (30%):
- Deep product knowledge
- Architecture understanding
- Technology landscape
- Database/infrastructure basics

Management Skills (40%):
- Communication
- Conflict resolution
- Feedback delivery
- Team motivation

Business Skills (30%):
- P&L management
- Hiring metrics
- OKRs and strategy
- Roadmap planning
```

### **Coaching Framework (1-on-1s)**

```
1-on-1 Meeting Structure (30-60 minutes):
1. Personal check-in (5 min)
2. Last week recap (5 min)
3. Blockers/issues (10 min)
4. Goals and progress (10 min)
5. Development plan (5-10 min)
6. Feedback exchange (5 min)

Feedback Model (SBI):
Situation - "In the code review yesterday..."
Behavior - "You pushed back on the architecture without..."
Impact - "...which made the team feel unheard"
```

---

## Developer Relations (DevRel)

### **Core Responsibilities**

1. **Community Building**
   - Build online communities (Discord, Slack)
   - Organize meetups and conferences
   - Forum moderation
   - User support

2. **Content Creation**
   - Blog posts and tutorials
   - Video tutorials and livestreams
   - Code examples and samples
   - API documentation

3. **Advocacy & Marketing**
   - Conference speaking
   - Thought leadership
   - Developer marketing
   - Brand building

4. **Feedback Loop**
   - Collect developer feedback
   - Report to product team
   - Feature advocacy
   - Customer success stories

### **Content Types**

```
Educational:
- Getting started guides
- API documentation
- Code patterns
- Best practices

Promotional:
- Case studies
- Customer stories
- "Built with..." features
- Product announcements

Community:
- Forum participation
- Event organization
- Sponsorships
- Developer meetups
```

### **DevRel Metrics**
- Community growth (Discord, GitHub followers)
- Content engagement (views, shares, comments)
- Speaking opportunities
- Developer satisfaction (surveys)

---

## Technical Writing

### **Core Responsibilities**

1. **Documentation Types**
   ```
   API Docs → Complete endpoint reference
   Tutorials → Step-by-step guides
   Guides → In-depth topics
   FAQs → Common questions
   Troubleshooting → Problem solutions
   ```

2. **Writing Best Practices**
   - Clear, concise language
   - Active voice
   - Short sentences
   - Consistent formatting
   - Real code examples

   **Good Example:**
   ```
   ✓ Run `npm install` to install dependencies.
   ✓ Use the POST /users endpoint to create users.
   ✓ Save your API key in a secure location.

   ✗ Dependencies should be installed via npm.
   ✗ POST /users can be utilized for user creation.
   ✗ API keys should be kept in a secure manner.
   ```

3. **Tools**
   - Markdown
   - Sphinx (Python)
   - MkDocs
   - Docusaurus
   - ReadTheDocs
   - GitHub Pages

4. **Documentation Site Structure**
   ```
   /docs
   ├── Getting Started
   ├── API Reference
   ├── Guides
   │   ├── Authentication
   │   ├── Rate Limiting
   │   └── Error Handling
   ├── Examples
   └── Troubleshooting
   ```

### **Technical Writing Checklist**
- [ ] Audience clearly defined
- [ ] Jargon minimized
- [ ] Code examples functional
- [ ] Consistent terminology
- [ ] Proper formatting
- [ ] Up-to-date information
- [ ] Search-friendly
- [ ] Mobile-responsive

---

## Quality Assurance (QA)

### **Testing Types**

**Unit Testing:**
```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, 5), 4)
```

**Integration Testing:**
```javascript
test('User registration flow', async () => {
  const response = await registerUser({
    email: 'test@example.com',
    password: 'secure123'
  });
  expect(response.status).toBe(201);

  const loginResponse = await login({
    email: 'test@example.com',
    password: 'secure123'
  });
  expect(loginResponse.user).toBeDefined();
});
```

**End-to-End Testing:**
```javascript
// Cypress
describe('Login flow', () => {
  it('should login successfully', () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('password');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

**Performance Testing:**
```bash
# Load testing with artillery
artillery load-test config.yml

# Results show:
# - Response times
# - Error rates
# - Throughput
```

### **QA Checklist**
- [ ] Functional testing complete
- [ ] Edge cases tested
- [ ] Performance acceptable
- [ ] Security vulnerabilities checked
- [ ] Cross-browser compatible
- [ ] Mobile responsive
- [ ] Accessibility standards met
- [ ] Documentation accurate

---

## Blockchain Development

### **Blockchain Fundamentals**

```solidity
// Solidity (Ethereum smart contract language)
pragma solidity ^0.8.0;

contract SimpleToken {
    mapping(address => uint256) public balances;
    string public name = "SimpleToken";
    uint256 public totalSupply = 1000000;

    constructor() {
        balances[msg.sender] = totalSupply;
    }

    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }

    function balance(address account) public view returns (uint256) {
        return balances[account];
    }
}
```

### **Token Standards**

```
ERC-20: Fungible tokens (like USD)
ERC-721: NFTs (non-fungible, unique)
ERC-1155: Multi-token standard (gaming)

DeFi: Decentralized Finance (lending, swaps)
DAOs: Decentralized Organizations
```

### **Web3 Stack**

```javascript
// Ethers.js (interacting with blockchain)
const { ethers } = require("ethers");

const provider = new ethers.providers.JsonRpcProvider(
  "https://mainnet.infura.io/v3/YOUR-API-KEY"
);

const balance = await provider.getBalance("0x...");
console.log(ethers.utils.formatEther(balance));

// Deploy contract
const Contract = await ethers.getContractFactory("MyToken");
const contract = await Contract.deploy();
await contract.deployed();
```

---

## Game Development

### **Game Engines**

**Unity:**
```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour {
    public float speed = 5f;
    private Rigidbody rb;

    void Start() {
        rb = GetComponent<Rigidbody>();
    }

    void Update() {
        float moveX = Input.GetAxis("Horizontal");
        float moveZ = Input.GetAxis("Vertical");

        Vector3 move = new Vector3(moveX, 0, moveZ) * speed;
        rb.velocity = move;
    }
}
```

**Godot:**
```gdscript
extends CharacterBody2D

export var speed = 200
var velocity = Vector2.ZERO

func _physics_process(delta):
    var input_vector = Vector2.ZERO
    input_vector.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
    input_vector.y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")

    if input_vector != Vector2.ZERO:
        velocity = input_vector.normalized() * speed
    else:
        velocity = Vector2.ZERO

    position += velocity * delta
```

### **Game Development Workflow**

```
Design → Programming → Art → Audio → Testing → Release
  ↓           ↓         ↓      ↓       ↓         ↓
GDD       Gameplay   Models  SFX    QA        Launch
          Physics    Textures Music   Polish   Monetize
          Collisions Materials Voice    UI      Updates
```

---

## Cybersecurity & Ethical Hacking

### **OWASP Top 10 Vulnerabilities**

```
1. SQL Injection
   ✗ SELECT * FROM users WHERE id = {user_input}
   ✓ SELECT * FROM users WHERE id = {parameterized_input}

2. Broken Authentication
   - Weak passwords
   - Session fixation
   - Insufficient MFA

3. Sensitive Data Exposure
   - Unencrypted data in transit
   - Weak cryptography
   - Missing HTTPS

4. XML External Entities (XXE)
   - Parsing untrusted XML
   - Solution: Disable external entity processing

5. Broken Access Control
   - Missing authorization checks
   - Privilege escalation
   - Horizontal/vertical access

6. Security Misconfiguration
   - Default credentials
   - Unnecessary services
   - Outdated software

7. Cross-Site Scripting (XSS)
   ✗ <h1>{userInput}</h1>
   ✓ <h1>{sanitizedInput}</h1>

8. Insecure Deserialization
   - Untrusted data deserialization
   - Remote code execution risk

9. Using Components with Known Vulnerabilities
   - Outdated libraries
   - Unpatched dependencies
   - Solution: Dependency scanning

10. Insufficient Logging & Monitoring
    - No audit trails
    - Missing alerts
    - Delayed detection
```

### **Penetration Testing Process**

```
1. Reconnaissance
   - Passive information gathering
   - Network mapping
   - Technology identification

2. Scanning
   - Port scanning (nmap)
   - Vulnerability scanning
   - Service enumeration

3. Enumeration
   - Detailed service probing
   - User enumeration
   - Share discovery

4. Exploitation
   - Exploit vulnerabilities
   - Gain access
   - Privilege escalation

5. Post-Exploitation
   - Maintain access
   - Collect evidence
   - Document findings

6. Reporting
   - Vulnerability summary
   - Risk assessment
   - Remediation recommendations
```

### **Security Tools**

```bash
# Network scanning
nmap -sV -A 192.168.1.1

# Web vulnerability
burp suite
owasp-zap

# Credential testing
hydra
john (password cracker)

# Protocol testing
wireshark (packet analysis)
metasploit (exploitation framework)
```

---

## UX/UI Design (For Technical Professionals)

### **Design Thinking Process**

```
Empathize → Define → Ideate → Prototype → Test
   ↓          ↓        ↓        ↓         ↓
Research   Problem  Brainstorm  Build    Validate
Users      Stmt.    Solutions   MVP      Feedback
```

### **UI Design Principles**

```
1. Consistency - Uniform design language
2. Hierarchy - Clear visual priority
3. Feedback - User actions have visible results
4. Constraints - Prevent invalid actions
5. Accessibility - Usable by everyone
```

### **Tools**

```
Figma, Sketch, Adobe XD - UI Design
Framer, Protopie - Prototyping
UsabilityHub - User testing
Storybook - Component documentation
```

---

## Career Transition Tips

**From Dev to Product Manager:**
- Master user empathy and metrics
- Learn about business models
- Understand competitive landscape
- Build cross-functional relationships

**From Dev to Engineering Manager:**
- Develop communication skills
- Learn performance management
- Understand team dynamics
- Take management training courses

**From Dev to DevRel:**
- Build personal brand
- Write quality content
- Speak at conferences
- Build communities

---

## Learning Checklist

Choose your specialization:

**Product Manager:**
- [ ] Understand product strategy
- [ ] Learn OKRs and metrics
- [ ] Know analytics tools
- [ ] Built a product roadmap

**Engineering Manager:**
- [ ] Developed communication skills
- [ ] Conducted training on management
- [ ] Shadowed experienced manager
- [ ] Led a small team project

**DevRel:**
- [ ] Written technical content
- [ ] Spoken at meetup/conference
- [ ] Built community presence
- [ ] Helped developers succeed

**Choose your path and commit!**

---

**Source**: https://roadmap.sh/product-manager, https://roadmap.sh/cyber-security, https://roadmap.sh/blockchain
