# Swift Coding Rules

Target Swift 6.2+ with strict concurrency. Use modern Swift Concurrency (`async`/`await`, actors) everywhere.

## Key principles

- No force unwraps (`!`) or force `try` unless truly unrecoverable — prefer `guard let`, `if let`, or `try?`/`do-catch`
- No GCD (`DispatchQueue`) — use `async`/`await` and actors
- Prefer `Double` over `CGFloat` (except with optionals / `inout`)
- Use `count(where:)` instead of `.filter { }.count`
- Use `Date.now` over `Date()`
- Prefer `if let value {` shorthand over `if let value = value {`
- Omit `return` in single-expression functions and computed properties
- Use `localizedStandardContains()` for user-input text filtering
- Never C-style number formatting (`String(format: "%.2f", x)`) — use `FormatStyle` APIs
- Prefer Swift-native string methods over Foundation equivalents

## Comprehensive review

For full Swift + SwiftUI best practices (deprecated API, performance, accessibility, data flow, navigation):
add `skills: [swiftui-pro]` to `claude-config.yaml`.
