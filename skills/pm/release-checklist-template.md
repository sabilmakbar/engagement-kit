# Release checklist: [artifact] v[X.Y.Z]

<!-- Closes every maintenance engagement (and any engagement that ships a release).
Two-key like every gate: machine key fully green BEFORE the human is asked. -->

## Machine key — all green before asking

- [ ] Full test suite green **in CI** (status fetched now; local runs never count)
- [ ] Every fixed finding has a named regression test that FAILS on the previous
      tag and passes on HEAD (run both sides)
- [ ] Version bumped: any payload edit since the last tag forces a bump — a
      released version number is never reused for different content
- [ ] Every manifest's version equals the intended tag
- [ ] Changelog diffed against merged PRs since the last tag — nothing missing
- [ ] No dev docs or untracked strays about to ship

## Human key

- [ ] User approves the release (standalone ask, never batched)

## Execute

- [ ] Tag created and pushed; GitHub release created; tag = release = manifest

## Post-release (dogfood — a release is not done until it survives real use)

- [ ] Real install/update on the actual machine (including the plugin half, if the
      artifact ships in two halves)
- [ ] Smoke run against real data; degraded states announce themselves loudly
- [ ] Deployed tree byte-matches the repo payload at the tag
- [ ] Parked and deferred items re-homed or explicitly re-parked
