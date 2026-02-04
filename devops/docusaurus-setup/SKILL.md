---
name: "docusaurus-setup"
description: "This skill use to deploy the Docusaurus site on github pages, deploy site to GitHub Pages using a CI/CD pipeline with the GitHub CLI."
version: "1.0.0"
---

# Docusaurus Setup Skill

## What This Skill Does

1.  **Project Analysis** - Examine Docusaurus structure and dependencies
2.  **Local Configuration Validation** - Verify Docusaurus config and sidebars
3.  **Local Build & Testing** - Build site locally and validate output
4.  **Content Verification** - Check for broken links and syntax errors
5.  **GitHub Pages Setup** - Configure repository and deployment settings
6.  **CI/CD Automation** - Set up GitHub Actions workflows
7.  **Deployment Verification** - Validate successful deployment

## When to Use This Skill

-   Deploy the Docusaurus site on github pages.
-   perform `git add .`, `git commit -m "update site - [detail]"` and `git push -u origin main` operation
-   You’re configuring if not already set `docusaurus.config.js` (title, baseUrl, theme plugins, navbar, footer).
-   You’re editing `sidebars.js` to match your course or project structure.
-   You need to set up deployment of a Docusaurus site to GitHub Pages with CI/CD.

## How This Skill Works
1.  **Confirm build output:**
    -   Run `npm run build` locally to ensure the site compiles without errors and outputs to `build/`.
    -   Fix any configuration issues (e.g., broken links or missing assets) before proceeding.

2.  **Configure `docusaurus.config.js`** if not already set:
    -   *Minimal Configuration Tip: Focus on `url`, `baseUrl`, `organizationName`, `projectName`, and `deploymentBranch` for initial setup.*
    -   Open `docusaurus.config.ts` and check these fields:
        -   `url`: Should be `https://<github-username>.github.io`.
        -   `baseUrl`: Should be `"/<repo-name>/"` if the project is not served from root.
        -   `organizationName` and `projectName`: Match your GitHub account and repository.
        -   `deploymentBranch`: Usually `gh-pages`.
        -   Optional fields like `trailingSlash`, `i18n` settings and `favicon` should reflect the project’s needs.
    -   Customize the navbar and footer links to mirror the course modules and external resources.
    -   Add or remove plugins (e.g., search, analytics) as needed for your use case.
    -   *Security Note: Avoid hardcoding sensitive information directly. Use environment variables (e.g., `.env` files or GitHub Secrets) for tokens or other confidential data.*

3.  **Edit `sidebars.js`**:
    -   *Minimal Configuration Tip: Define a basic structure with your main content categories.*
    -   Define the sidebar structure to reflect the course outline or document hierarchy.
    -   Group chapters and sections logically, using categories for modules and weeks.
    -   Ensure that sidebars update automatically when new Markdown/MDX files are added.

4.  **Theme customization**:
    -   Adjust styling via `@theme` components or CSS for consistent colors and typography.
    -   Override theme components in the `src/theme` directory (e.g., custom layout or code block styles).
    -   Test changes locally using `npm run start` to ensure responsiveness.

5.  **Prepare for GitHub Pages deployment**:
    -   Initialize a Git repository and connect it to GitHub using the GitHub CLI (e.g., `gh repo create <repo> --public`).
    -   Push the initial site to the repository.
    -   In `docusaurus.config.js`, set the `organizationName`, `projectName`, and `deploymentBranch` fields to match your GitHub org/user and repository.
    -   *Important: If GitHub Pages is not yet enabled for your repository, run `gh pages enable --branch gh-pages` via the GitHub CLI.*

6.  **Set up CI/CD pipeline**:
    -   Check if `.github/workflows/deploy.yml` exists in the repository.
    -   If it doesn’t exist or needs updating, create it with a workflow similar to:
    ```yaml
      name: Deploy Docusaurus to GitHub Pages
      on:
        push:
          branches:
            - main
      jobs:
        build:
          runs-on: ubuntu-latest
          steps:
          - uses: actions/checkout@v3
          - uses: actions/setup-node@v3
            with:
              node-version: '18'
          - run: npm ci
          - run: npm run build
          - uses: peaceiris/actions-gh-pages@v3
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}
              publish_dir: ./build
              publish_branch: gh-pages
      ```
      1.  Checks out the repository.
      2.  Installs Node dependencies (e.g., using `actions/setup-node`).
      3.  Builds the static site (`npm run build`).
      4.  Deploys the contents of `build` to the `gh-pages` branch using `actions-gh-pages` or `gh` CLI.
    -   Commit and push the workflow to the default branch; GitHub Actions will handle future deployments on push.

7.  **Deployment Verification (New Content/Updates)**:
    -   Run `npm run start` locally to verify site appearance.
    -   **Commit your changes:**
        -   `git add .`
        -   `git commit -m "Update site - [detail of changes]"`
        -   `git push origin main` (or your default branch)
    -   After the GitHub Actions workflow finishes, the site will be available at `https://<username>.github.io/<repo>/`.
    -   Make adjustments to configuration files if deployment fails (e.g., baseUrl mismatch).
    -   Once completed, visit `https://<github-username>.github.io/<repo-name>/` to confirm your updated book is live.

8.  **Ongoing usage:**
    -   Each time new content is committed, the workflow automatically redeploys the site.

## Performance Targets

-   **Build time**: < 30 seconds (typical)
-   **Page load**: < 3 seconds
-   **Bundle size**: Optimized for documentation
-   **Accessibility**: WCAG 2.1 AA compliance

## Quality Gates (Constitution v3.1.2)

Before deployment to production, verify:
-   [ ] All content passes validation-auditor validation
-   [ ] Local build completes without errors
-   [ ] No broken links or missing resources
-   [ ] TypeScript type checking passes
-   [ ] Performance targets met
-   [ ] Accessibility standards verified
-   [ ] GitHub Actions workflow configured correctly


## Output Format

When using this skill, provide:

-   A clear **repository name** and the **desired site name**.
-   Any **custom sections or modules** to include in `sidebars.js`.
-   Details about **theme changes** (e.g., custom color palette, fonts).
-   Confirmation that the GitHub CLI is authenticated on your machine.

The skill will return:

1.  **Project Setup Summary**: Path to the new Docusaurus project and commands executed.
2.  **Configuration Details**: A checklist of changes made to `docusaurus.config.js` and `sidebars.js`.
3.  **Confirmation Deploy.yml**: Confirmation of whether `.github/workflows/deploy.yml` already existed or was created.
4.  **CI/CD Instructions**: A ready-to-commit `deploy.yml` workflow for GitHub Actions and notes on enabling GitHub Pages.
5.  **Next Steps**: 
  - First find the Docusaurus project folder `cd <project_folder_name>` 
  - How to add content to the `docs` or `blog` folders inside Docusaurus project and verify deployment.

## Example

**Input:** “I just added a new chapter and want to publish the updated Docusaurus site.”

**Output:**
-   **Config Check:** Verified `url` is `https://jane-doe.github.io`, `baseUrl` is `/physical-ai-book/`, and `deploymentBranch` is `gh-pages`. No changes needed.
-   **Configuration Details**: Updated site title to “Robotics Course Book,” , added modules to `sidebars.js` (Module 1: ROS 2, Module 2: Digital Twin…).
-   **Workflow Creation:** Added `.github/workflows/deploy.yml` for automatic deployment on pushes to `main`.
-   **Next Steps:** Add your markdown chapters to `docs/`,Run `npm run build` locally if desired, **commit all changes (`git add .` and `git commit -m "Add Chapter 3 and deployment pipeline"`), and push (`git push origin main`)**. After the GitHub Actions workflow finishes, the site will be available at `https://<github-username>.github.io/physical-ai-book/`.
