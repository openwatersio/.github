# Marketing skills

Everyone doing marketing work for Open Waters uses the relevant skills from [Corey Haines's Marketing Skills](https://github.com/coreyhaines31/marketingskills). This applies across the organization, including work in product and library repositories. Agents read and apply the matching skill before starting the task, without waiting for someone to request it by name.

## Setup

Install the collection using the [upstream installation instructions](https://github.com/coreyhaines31/marketingskills#installation). The cross-agent installer is:

```sh
npx skills add coreyhaines31/marketingskills
```

Select each agent harness you use when prompted. When installing from an agent session, pass the target agent explicitly; upstream documents `-a claude-code` for Claude Code. An existing installation of the `marketing-skills` plugin also satisfies this requirement. Confirm the relevant skills are available in your harness before starting marketing work.

If your harness cannot load skills, read the relevant upstream `skills/<name>/SKILL.md` and its referenced resources directly. Keep upstream as the source for the collection; keep Open Waters conventions here.

## Use in everyday work

Start with the product's existing audience, positioning, and goals. The `product-marketing` skill maintains that context in `.agents/product-marketing.md`; reuse it across related work and update it when the product or audience changes. Confirm product claims against the repository and shipped behavior.

Choose skills by the task. Common examples are `copywriting` and `copy-editing` for landing pages, `seo-audit` for search visibility, `aso` for App Store listings, `launch` for announcements, `pricing` for packaging, `onboarding` for activation flows, and `analytics` for measurement. Consult the [upstream skill catalog](https://github.com/coreyhaines31/marketingskills#available-skills) for other tasks and follow each skill's related-skill guidance.

Apply the shared [writing style](writing-style.md) to the resulting copy, including its humanizer pass. Repository-specific facts and the user's instructions still govern the work.

## Repository instructions

Link this page from each repository's `CONTRIBUTING.md` so humans and agents discover the same expectation:

```markdown
Use the relevant [marketing skills](https://github.com/openwatersio/.github/blob/main/docs/agents/marketing.md) for marketing work, including copy, SEO, App Store listings, launches, pricing, onboarding, and analytics.
```
