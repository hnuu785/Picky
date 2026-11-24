import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = { title: "Picky" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
