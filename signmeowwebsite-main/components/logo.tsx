export function SignMeowLogo({ className = "w-10 h-10" }: { className?: string }) {
  return (
    <div className={`${className} relative`}>
      <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
        {/* Cat head - main circle */}
        <circle cx="20" cy="22" r="14" fill="url(#gradient1)" className="drop-shadow-sm" />

        {/* Cat ears - triangular shapes */}
        <path d="M12 12 L8 4 L16 8 Z" fill="url(#gradient2)" className="drop-shadow-sm" />
        <path d="M28 12 L32 4 L24 8 Z" fill="url(#gradient2)" className="drop-shadow-sm" />

        {/* Inner ears */}
        <path d="M12 12 L10 6 L14 9 Z" fill="#f97316" opacity="0.6" />
        <path d="M28 12 L30 6 L26 9 Z" fill="#f97316" opacity="0.6" />

        {/* Eyes - clean circles */}
        <circle cx="16" cy="20" r="2" fill="#1e293b" />
        <circle cx="24" cy="20" r="2" fill="#1e293b" />

        {/* Eye highlights */}
        <circle cx="16.5" cy="19.5" r="0.5" fill="white" />
        <circle cx="24.5" cy="19.5" r="0.5" fill="white" />

        {/* Nose - diamond shape */}
        <path d="M20 24 L18 26 L20 28 L22 26 Z" fill="#e11d48" />

        {/* Mouth - curved lines */}
        <path d="M20 28 Q16 30 14 28" stroke="#1e293b" strokeWidth="1.5" strokeLinecap="round" fill="none" />
        <path d="M20 28 Q24 30 26 28" stroke="#1e293b" strokeWidth="1.5" strokeLinecap="round" fill="none" />

        {/* Whiskers */}
        <line x1="8" y1="22" x2="12" y2="21" stroke="#1e293b" strokeWidth="1" strokeLinecap="round" />
        <line x1="8" y1="25" x2="12" y2="24" stroke="#1e293b" strokeWidth="1" strokeLinecap="round" />
        <line x1="32" y1="22" x2="28" y2="21" stroke="#1e293b" strokeWidth="1" strokeLinecap="round" />
        <line x1="32" y1="25" x2="28" y2="24" stroke="#1e293b" strokeWidth="1" strokeLinecap="round" />

        {/* Gradients */}
        <defs>
          <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fb923c" />
            <stop offset="100%" stopColor="#f97316" />
          </linearGradient>
          <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fb923c" />
            <stop offset="100%" stopColor="#ea580c" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  )
}
