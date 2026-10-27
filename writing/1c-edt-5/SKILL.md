---
name: '1C EDT: транзакции и блокировки'
description: >-
  Use when writing posting, bulk updates, or locks in a 1C:EDT project:
  transactions, managed locks, register writes, and balance control.
---
# 1C EDT: транзакции и блокировки

Apply when writing posting, bulk updates, or any write path in a 1C:EDT project (object modules and server common modules under `src/`, register properties in `.mdo`). Checklist distilled from ITS v8std, not a copy of the articles.

## Transactions (№783)

- Every begin has a commit or a rollback, in the same method.
- After begin, the work sits in one `Попытка`. Commit is the last statement inside it.
- On failure, roll back first. If the exception must leave the method, raise it again after the rollback.
- Do not touch the database while a transaction is still open after an error.
- A transaction wraps one indivisible business action. Keep it short. On a busy system a portion should finish in about 20 seconds.
- No external calls and no optional heavy calculation inside the transaction.

## Managed locks (№460, №648, №490)

- The configuration uses managed locks.
- If you read data and then change it, take an explicit managed lock before the read, for the rest of the transaction.
- An exclusive lock when the read is followed by a write. A shared lock on what you only read, and an exclusive lock on what you change, when the read must stay true but that set itself is not written.
- Lock only the rows you actually process.
- Do not use `ДЛЯ ИЗМЕНЕНИЯ` in managed mode.
- A read is “responsible” when its result changes data or decides a write. Lists, search, most reports, and nearly static data are not responsible reads.
- Do not open another transaction inside a handler that already runs in a platform transaction.
- Before changing an existing reference object from code, lock it with `Заблокировать` or `ЗаблокироватьДанныеДляРедактирования`. A form already locks its main object.
- On a lock conflict, tell the user or skip the object and retry later.
- Skip that object lock in a job that must beat the user, or in a mode that is already exclusive.
- Before changing a reference object, add the object lock on top of the data lock.

## Reads and register writes (№496, №792, №497)

- Read a few attributes with a query or the standard attribute helper. Do not load the whole object through the reference.
- Do not write a register set one row per loop. Write batches, about 1000 rows per call.
- If you change no more than about 30% of a large set, write the difference, not the whole set. Compute the difference with a query and use the batch replace modes.
- Append with add. Other cases use merge, delete, or update, matching the platform version.
- For a recorder-subordinate register, compare rows without the line number and pick update, delete, or add from what actually changed.
- When a user action writes an object, also record it in `ИсторияРаботыПользователя` with the navigation link, if that history is part of the configuration.

## Excess locks (№659, №662, №663, №664, №661)

- Design metadata so sessions do not fight over the same resource. Look hard at sequences, accounting registers, and accumulation registers. Wait appears when two sessions need one resource.
- Do not move a sequence boundary while posting. Do it in a scheduled job. One dimension set of a sequence is a single resource and serializes users.
- For busy operational posting, enable totals splitting on accounting and accumulation registers: allow it in metadata, then turn it on in the infobase. Splitting does not remove locks caused by balance control.
- Choose accumulation dimensions for the parallelism you need. Add splitting only if dimensions are not enough.
- Run balance control as late in the transaction as you can.
- If a negative balance is forbidden, read balances with a lock. Two sessions must not read the same balance at once.
- Check only balances that can actually go negative.
- At the start of the transaction, write registers that are not balance-checked, in a stable order.
- Write balance-checked registers at the end, with `БлокироватьДляИзменения = Истина`.
- Roll back if a balance went negative. Commit if the check is empty.
- In automatic lock mode, do not add another `ДЛЯ ИЗМЕНЕНИЯ` when the write already locked those balances.

## Sources

- https://its.1c.ru/db/v8std/content/783/hdoc
- https://its.1c.ru/db/v8std/content/460/hdoc
- https://its.1c.ru/db/v8std/content/490/hdoc
- https://its.1c.ru/db/v8std/content/648/hdoc
- https://its.1c.ru/db/v8std/content/496/hdoc
- https://its.1c.ru/db/v8std/content/497/hdoc
- https://its.1c.ru/db/v8std/content/792/hdoc
- https://its.1c.ru/db/v8std/content/659/hdoc
- https://its.1c.ru/db/v8std/content/662/hdoc
- https://its.1c.ru/db/v8std/content/663/hdoc
- https://its.1c.ru/db/v8std/content/664/hdoc
- https://its.1c.ru/db/v8std/content/661/hdoc
