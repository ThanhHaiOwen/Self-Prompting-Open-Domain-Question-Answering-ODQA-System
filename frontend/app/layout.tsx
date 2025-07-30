import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Self-Prompting ODQA System',
  description: 'A complete implementation of Self-Prompting Large Language Models for Zero-Shot Open-Domain QA',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
