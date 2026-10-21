Notes: 



**1. python interpreter:**

Then point VS Code at it: press Cmd+Shift+P (Ctrl+Shift+P), run "Python: Select Interpreter," and pick the one with .venv in its path. This lets VS Code autocomplete and check your code properly.

**2. Save and push to GitHub**

bash
pip freeze > requirements.txt
git add .
git commit -m "FastAPI app with health endpoint and first test"
git push

This is the loop you'll use for the whole project:

git add . stages your changes, picking which ones to save.
git commit -m "..." saves a snapshot with a message describing what you did.
git push uploads your commits to GitHub.