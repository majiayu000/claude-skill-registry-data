---
name: omadiki-ergasia-git
description: Οργάνωση ομαδικής φοιτητικής εργασίας λογισμικού με Git και GitHub/GitLab - στήσιμο repo, branches, pull requests, κανόνες commit, επίλυση συγκρούσεων (merge conflicts), μοιρασιά εργασιών, .gitignore και διάσωση από συνηθισμένα λάθη Git. Use for team projects, ομαδική εργασία, git help, merge conflict, "χάλασα το git", undo commit, pull request, branching strategy, GitHub Classroom.
---

# Ομαδική εργασία με Git

Μιλάς στα ελληνικά, με εντολές που αντιγράφονται αυτούσιες. Πριν από **οποιαδήποτε εντολή που σβήνει δουλειά** (`reset --hard`, `push --force`, `clean -fd`, `branch -D`), εξηγείς τι θα χαθεί και προτείνεις πρώτα backup branch. Αν έχεις πρόσβαση σε shell, δεν τις εκτελείς χωρίς ρητή έγκριση.

## 1. Στήσιμο (μία φορά, από έναν της ομάδας)

```bash
git init -b main
# .gitignore ανάλογα με τη γλώσσα (δες παρακάτω)
git add . && git commit -m "Αρχική δομή έργου"
gh repo create <όνομα> --private --source=. --push   # ή μέσω της σελίδας του GitHub
```

Μετά, στο GitHub: Settings → Collaborators (πρόσκληση μελών), Settings → Branches → προστασία του `main` (απαιτείται pull request).

### Ελάχιστο .gitignore

```gitignore
# Γενικά
.DS_Store
Thumbs.db
.idea/
.vscode/
*.log
.env
# C / C++
*.o
*.out
build/
# Python
__pycache__/
.venv/
*.pyc
# Java
*.class
target/
# Node
node_modules/
dist/
# LaTeX
*.aux
*.bbl
*.blg
*.synctex.gz
_minted-*/
```

**Ποτέ στο repo:** κωδικοί, API keys, `.env`. Αν μπήκε κατά λάθος, το κλειδί θεωρείται διαρρεύσαν: **ακυρώνεται** και εκδίδεται νέο. Η διαγραφή από το ιστορικό δεν αρκεί.

## 2. Ροή εργασίας (GitHub Flow, απλή και αρκετή για φοιτητές)

```bash
git switch main && git pull                 # πάντα από ενημερωμένο main
git switch -c feature/parser                # ένα branch ανά εργασία
# ... δουλειά ...
git add -p                                  # διάλεξε τι μπαίνει στο commit
git commit -m "Προσθήκη parser για αρχεία εισόδου"
git push -u origin feature/parser
gh pr create --fill                         # ή από το GitHub
```

Κανόνες ομάδας (πρότεινε να μπουν στο README):
- Κανένα απευθείας push στο `main`.
- Κάθε PR το εγκρίνει τουλάχιστον ένα **άλλο** μέλος (δες `requesting-code-review`, `receiving-code-review`).
- Μικρά PR (< 300 γραμμές). Ένα PR = ένα θέμα.
- Τα tests περνούν πριν το merge (ιδανικά με GitHub Actions).

### Καλά μηνύματα commit

- Προστακτική ή ουσιαστικό, σύντομο θέμα: «Διόρθωση off-by-one στη δυαδική αναζήτηση».
- Όχι «fix», «αλλαγές», «asdf», «τελικό τελικό v3».
- Αν χρειάζεται, κενή γραμμή και εξήγηση του *γιατί*.

## 3. Μοιρασιά εργασίας

- Σπάσε την εργασία σε issues στο GitHub, με υπεύθυνο και προθεσμία.
- Συμφωνήστε **διεπαφές** (υπογραφές συναρτήσεων, μορφή δεδομένων) πριν δουλέψει ο καθένας χωριστά. Έτσι αποφεύγονται τα περισσότερα conflicts.
- Εβδομαδιαίο 15λεπτο: τι έκανα, τι θα κάνω, τι με εμποδίζει.
- Το `git log --author` και τα PR δείχνουν ποιος έκανε τι. Αυτό βοηθά και όταν ο διδάσκων ζητά ατομική συνεισφορά.

## 4. Συγκρούσεις (merge conflicts)

```bash
git switch feature/parser
git fetch origin
git merge origin/main          # ή: git rebase origin/main (αν η ομάδα το προτιμά)
# Άνοιξε τα αρχεία με <<<<<<< ======= >>>>>>>, κράτα το σωστό, σβήσε τα σημάδια
git add <αρχεία> && git commit # (σε rebase: git rebase --continue)
```

Όταν βοηθάς σε conflict: εξήγησε τι άλλαξε η κάθε πλευρά και γιατί συγκρούονται, και μην επιλέγεις στα τυφλά «ours/theirs». Αν δεν είναι σαφές, ρώτα ποιος έγραψε τον κώδικα και τι ήθελε.

## 5. Διάσωση: «χάλασα το git»

| Πρόβλημα | Λύση |
|---|---|
| Λάθος μήνυμα στο τελευταίο commit (όχι pushed) | `git commit --amend` |
| Ξέχασα ένα αρχείο στο τελευταίο commit | `git add f && git commit --amend --no-edit` |
| Αναίρεση τελευταίου commit, κρατώντας τις αλλαγές | `git reset --soft HEAD~1` |
| Αναίρεση commit που έχει ήδη γίνει push | `git revert <hash>` (ασφαλές, δεν ξαναγράφει ιστορικό) |
| Έκανα commit στο main αντί σε branch (όχι pushed) | `git branch feature/x && git reset --keep origin/main && git switch feature/x` (το commit μένει στο νέο branch) |
| Θέλω να πετάξω τις αλλαγές σε ένα αρχείο | `git restore <αρχείο>` ⚠️ χάνονται |
| «Έχασα» commits μετά από reset | `git reflog` → βρες το hash → `git branch rescue <hash>` |
| Αποθήκευση αλλαγών προσωρινά | `git stash` / `git stash pop` |
| `push rejected (non-fast-forward)` | `git pull --rebase` και μετά `git push`. **Όχι** `--force` σε κοινό branch |
| Μπήκε κωδικός/κλειδί σε commit | Ακύρωσέ το αμέσως στην υπηρεσία. Μετά καθαρισμός με `git filter-repo` |

Πριν από επικίνδυνη εντολή: `git branch backup-$(date +%s)`.

## 6. Για εργαλεία του Claude Code

Για ανεξάρτητα features δίπλα-δίπλα δες `using-git-worktrees`. Για το κλείσιμο ενός branch, `finishing-a-development-branch`. Για εργασίες με το `gh`, το `gh-cli`.
