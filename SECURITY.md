# Security and responsible use

## Credentials

Keep `OPENROUTER_API_KEY` in a local `.env` or process environment. Commit only `.env.example` with its placeholder. Inspect staged changes before publishing, including screenshots and terminal output.

If a key is exposed, revoke or rotate it through its provider immediately. Removing it from the current file does not remove it from Git history. Notify the repository owner privately through an available private GitHub channel; do not post a token in a public issue. This project does not publish a dedicated security email or response-time commitment.

## Data and model behavior

- Full RAG sends the question and retrieved text to OpenRouter and the hosted inference path. Review service terms before submitting sensitive content.
- Use public, non-sensitive demonstration material. There is no redaction, access control, or document-level permissions.
- Retrieved documents are inserted directly into prompts. No prompt-injection defense is implemented.
- Generated text and citation labels can be incorrect. Compare claims with displayed sources.
- Supplied notes lack external evidence. Verify real business decisions against suitable current sources.

## Supported scope

This is an experimental CLI with no production security support commitment. Dependency versions document the local environment; they do not certify an audit. Report defects with the script, sanitized reproduction steps, and dependency/Python versions.
