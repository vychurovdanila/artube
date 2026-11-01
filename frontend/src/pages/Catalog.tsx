const MOCK_ITEMS = [
  { id: 1, title: '2017 Porsche Macan', img: '/assets/1.webp' },
  { id: 2, title: '2017 Porsche Macan', img: '/assets/17.webp' },
  { id: 3, title: '2017 Porsche Macan', img: '/assets/18.webp' },
  { id: 4, title: '2017 Porsche Macan', img: '/assets/19.webp' },
  { id: 5, title: '2017 Porsche Macan', img: '/assets/20.webp' },
  { id: 6, title: '2017 Porsche Macan', img: '/assets/Frame%207.jpg' },
];

export default function Catalog() {
  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {MOCK_ITEMS.map((item) => (
          <div key={item.id} className="group cursor-pointer">
            <div className="aspect-[4/3] bg-gray-100 rounded-xl overflow-hidden mb-3 relative">
              <img src={item.img} alt={item.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" onError={(e) => { e.currentTarget.src = 'https://via.placeholder.com/600x400?text=No+Image'; }} />
            </div>
            <div className="flex items-center justify-between px-1">
              <div className="flex items-center gap-2 text-sm font-bold text-gray-800">
                <span className="text-blue-500 text-lg">»</span>
                {item.title}
              </div>
              <div className="flex items-center gap-3 text-gray-400">
                <svg className="w-5 h-5 hover:text-black cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                <svg className="w-5 h-5 hover:text-black cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                <svg className="w-5 h-5 text-blue-500 cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path></svg>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
