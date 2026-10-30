# Setup — Install & Authentication

Load this when `which sonar` finds nothing, or when `sonar auth status` shows no connection to the DVLA server.

**Server:** `https://sonarqube.tooling.dvla.gov.uk/`

---

## CLI Not Installed

If `which sonar` finds nothing, guide the user to install it:

```
Install the SonarQube CLI:

  # Linux / macOS
  curl -o- https://raw.githubusercontent.com/SonarSource/sonarqube-cli/refs/heads/master/user-scripts/install.sh | bash

  # Windows (PowerShell)
  irm https://raw.githubusercontent.com/SonarSource/sonarqube-cli/refs/heads/master/user-scripts/install.ps1 | iex
```

Docs: https://docs.sonarsource.com/sonarqube-cli · Commands:
https://www.sonarsource.com/sonarqube/cli/commands.html

---

## Authentication

> **Agents cannot authenticate.** `sonar auth login` opens a browser and stores a
> token in the system keychain — it MUST be run by the user, not the agent.

If `sonar auth status` shows no connection, stop and ask the user to run:

```
sonar auth login --server https://sonarqube.tooling.dvla.gov.uk/
```

Once they confirm, re-run `sonar auth status` and continue. After login, all
commands (including `sonar api`) use the stored credentials automatically — you
never handle the token directly.

Verify with:

```
sonar auth status
```

---

## Safety

- **Never run `sonar auth login` yourself** — only the user can authenticate.
- **Never print or store the auth token.** `sonar api` uses the keychain; you
  don't need the raw token.
