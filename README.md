# Communication

The app is master and cap is slave.

## Finite State Automaton

```mermaid
graph TD;
  Z[idle];
  A[ready];
  B[pouring];
  C[check];

  Z -->|connect| A;

  A -->|disconnect| Z;
  
  A -->|pour| B;

  B -->|till| B;

  B -->|finish| A;

  A -->|ping| C;
  C -->|pong| A;
```

## Protocol

Each action must end with a stop from the cap.