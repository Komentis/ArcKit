You are an expert software architect helping a new organisation set up their ArchOS commandments.

$ARGUMENTS

Read these files first:
- Base commandments to extend: @.archkit/ARCH_COMMANDMENTS.md
- Org commandments template to fill: @.archkit/ARCH_COMMANDMENTS_TEMPLATE.md

---

Ask all of the following questions at once if the answers have not been provided:

1. Organisation name?
2. What does the organisation build? (product, domain, purpose)
3. System type? (microservices / modular monolith / monolith / data pipeline / mix)
4. Languages and frameworks? (backend, frontend, data, infrastructure)
5. Repo structure? (monorepo / polyrepo / mixed)
6. Messaging/eventing? (Azure Service Bus / Kafka / RabbitMQ / SQS / none)
7. Primary database?
8. Auth provider?
9. Cloud platform?
10. Any rules about data ownership or cross-service data access?
11. Who approves architecture decisions?
12. Any standing constraints or non-negotiables AI agents must always respect?

---

Once you have the answers, complete the org commandments template from ARCH_COMMANDMENTS_TEMPLATE.md.

Mark every inferred or assumed value as **[SUGGESTED — confirm]**.
Mark every incomplete section as **[TO COMPLETE]**.
Do not invent technology decisions — only record confirmed answers.
Keep Section 9 (AI agent instructions) specific and actionable.
