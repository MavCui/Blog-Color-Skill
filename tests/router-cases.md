# Router review cases

These cases record expected behavior for manual conversational evaluation. They are not automated model evaluations.

1. Topic only: AI memory → ask for missing title and placement; offer three distinct compatible proposals.
2. Full Chinese article on context boundaries → preserve the article title and extract one central relationship.
3. English essay on design process → retain English wording and offer language-appropriate type.
4. Feishu 5:1 brief → every proposal places essential content in the central safe region.
5. Exact brand color → retain the supplied color in all proposals and explain its role.
6. Series continuation → reuse the explicitly saved series; vary subject without changing its identity.
7. One-off change inside a series → do not silently overwrite its stored profile.
8. Existing portrait as subject → preserve its identity; classify it as an edit target.
9. Reference image for style only → extract visual grammar without copying subject or layout.
10. User selected Swiss → show compatible type and palette variants, without forcing other families.
11. Long exact Chinese headline → preserve text; offer a shorter title if the safe area cannot contain it.
12. User asks to generate directly → skip proposal waiting, preserve exact constraints, and generate.
