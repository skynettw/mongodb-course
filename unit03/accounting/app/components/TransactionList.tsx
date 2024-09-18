import React from 'react';

interface Transaction {
  id: string;
  summary: string;
  // ... 其他必要的屬性
}

interface TransactionListProps {
  transactions: Transaction[];
}

function TransactionList({ transactions }: TransactionListProps) {
  return (
    <ul>
      {transactions.map((transaction) => (
        <li key={transaction.id}>
          {/* ... 其他欄位 ... */}
          <span className="summary">{transaction.summary}</span>
          {/* ... 其他欄位 ... */}
        </li>
      ))}
    </ul>
  );
}

export default TransactionList;