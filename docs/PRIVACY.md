# Privacy Notice

Last updated: 2026-04-26

This file explains data handling expectations for this repository's default implementation.

## Data flow in current scaffold

- CLI path (`main.py`): user input is processed in-memory for the active process.
- HTTP bridge (`bridge/http_server.py`): request payloads are processed in-memory and routed to session state.
- Session state: message history is kept in process memory while the process is running.

## What is not included by default

- No built-in database persistence.
- No built-in user account system.
- No built-in analytics pipeline.

## External model providers

If `OPENAI_API_KEY` (or other provider credentials) is configured, message content may be sent to external APIs.
Those providers process data under their own terms and privacy policies.
You are responsible for reviewing and complying with those policies.

## Operator responsibilities

If you deploy or modify this project, you are responsible for:

- Providing a clear user-facing privacy notice.
- Defining lawful data basis and retention practices.
- Applying access controls and security safeguards.
- Managing deletion and incident response processes.
- Meeting applicable regulations (for example, GDPR, HIPAA, or local equivalents where applicable).

## Sensitive information warning

Do not input secrets or highly sensitive personal data unless your deployment has appropriate controls.

## Not legal advice

This notice is a technical baseline, not legal advice.
Consult qualified legal counsel before production deployment.

