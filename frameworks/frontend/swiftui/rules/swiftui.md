# SwiftUI Rules

Target iOS 26+ / SwiftUI with Swift 6.2. Avoid UIKit unless explicitly requested.

## Architecture

- Use `@Observable` + `@MainActor` for shared state (not `ObservableObject` / `@Published`)
- Pass state with `@State` (ownership), `@Bindable` / `@Environment` (passing)
- Keep view `body` thin — move logic to methods or view models
- One type per Swift file; break long `body` into extracted `View` structs

## Modern API

- `NavigationStack` / `NavigationSplitView` — never `NavigationView`
- `navigationDestination(for:)` — never `NavigationLink(destination:)`
- `foregroundStyle()` — never `foregroundColor()`
- `clipShape(.rect(cornerRadius:))` — never `.cornerRadius()`
- `Tab` API — never `tabItem()`
- `@Observable` / `@Entry` macro — never manual `EnvironmentKey` pattern

## Animations

- `.animation(.bouncy, value: x)` — never `animation(_:)` without a value
- Use `@Animatable` macro instead of manual `animatableData`
- Chain animations via `withAnimation { } completion: { }`, not delayed `withAnimation` calls

## Performance

- Prefer ternary over `if/else` view branching to preserve structural identity
- Avoid `AnyView` — use `@ViewBuilder`, `Group`, or generics
- Use `task()` over `onAppear()` for async work (auto-cancelled on disappear)
- `LazyVStack`/`LazyHStack` for large data sets in `ScrollView`

## Comprehensive review

For the full expert-level SwiftUI review including accessibility, deprecated API, navigation, data flow, and performance:
add `skills: [swiftui-pro]` to `claude-config.yaml`.
