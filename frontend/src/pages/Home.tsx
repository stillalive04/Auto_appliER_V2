import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const Home = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    setIsLoaded(true)
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 2 - 1,
        y: (e.clientY / window.innerHeight) * 2 - 1
      })
    }
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 overflow-hidden relative">
      {/* 3D Mountain Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Mountain Layers */}
        <div 
          className="absolute bottom-0 left-0 right-0 h-96 bg-gradient-to-t from-slate-800 to-transparent"
          style={{
            clipPath: 'polygon(0 100%, 20% 60%, 40% 80%, 60% 40%, 80% 70%, 100% 20%, 100% 100%)',
            transform: `translateX(${mousePosition.x * 15}px) translateY(${mousePosition.y * 8}px)`
          }}
        />
        <div 
          className="absolute bottom-0 left-0 right-0 h-80 bg-gradient-to-t from-purple-800/60 to-transparent"
          style={{
            clipPath: 'polygon(0 100%, 15% 70%, 35% 90%, 55% 50%, 75% 80%, 90% 30%, 100% 100%)',
            transform: `translateX(${mousePosition.x * -12}px) translateY(${mousePosition.y * 6}px)`
          }}
        />
        <div 
          className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-slate-700/40 to-transparent"
          style={{
            clipPath: 'polygon(0 100%, 25% 80%, 45% 95%, 65% 60%, 85% 85%, 100% 40%, 100% 100%)',
            transform: `translateX(${mousePosition.x * 8}px) translateY(${mousePosition.y * 4}px)`
          }}
        />
        <div 
          className="absolute bottom-0 left-0 right-0 h-48 bg-gradient-to-t from-cyan-900/30 to-transparent"
          style={{
            clipPath: 'polygon(0 100%, 30% 90%, 50% 70%, 70% 85%, 90% 60%, 100% 100%)',
            transform: `translateX(${mousePosition.x * -6}px) translateY(${mousePosition.y * 3}px)`
          }}
        />
        
        {/* Animated Stars */}
        <div className="absolute inset-0">
          {[...Array(100)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 60}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 2}s`
              }}
            />
          ))}
        </div>
        
        {/* Floating Clouds */}
        <div className="absolute inset-0 opacity-20">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="absolute w-40 h-20 bg-white rounded-full blur-sm animate-pulse"
              style={{
                left: `${10 + i * 20}%`,
                top: `${15 + i * 8}%`,
                animationDelay: `${i * 3}s`,
                animationDuration: `${8 + i * 2}s`,
                transform: `translateX(${mousePosition.x * (i + 1) * 3}px) scale(${0.8 + i * 0.1})`
              }}
            />
          ))}
        </div>
        
        {/* Aurora Effect */}
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            background: `linear-gradient(45deg, 
              rgba(0, 255, 255, 0.1) 0%, 
              rgba(128, 0, 255, 0.1) 25%, 
              rgba(255, 0, 128, 0.1) 50%, 
              rgba(0, 255, 255, 0.1) 75%, 
              rgba(128, 0, 255, 0.1) 100%)`,
            transform: `translateX(${mousePosition.x * 20}px) translateY(${mousePosition.y * 10}px)`
          }}
        />
      </div>

      {/* Navigation */}
      <nav className="relative z-50 bg-black/10 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <div className="h-10 w-10 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-xl flex items-center justify-center transform rotate-12 hover:rotate-0 transition-transform duration-300">
                    <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div className="absolute -inset-1 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-xl blur opacity-25 animate-pulse"></div>
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                  AutoJobApply
                </h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                to="/login" 
                className="text-white/80 hover:text-white px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 hover:bg-white/10 backdrop-blur-sm"
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className="relative group bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-400 hover:to-purple-400 text-white px-6 py-2 rounded-xl text-sm font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-cyan-500/25"
              >
                <span className="relative z-10">Get Started Free</span>
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-purple-600 rounded-xl blur opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className={`text-center transform transition-all duration-1000 ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          <div className="mb-8">
            <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/30 backdrop-blur-sm">
              🚀 AI-Powered Job Automation
            </span>
          </div>
          
          <h1 className="text-6xl md:text-8xl font-bold text-white mb-8 leading-tight">
            <span className="block">Land Your</span>
            <span className="block bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-pulse">
              Dream Job
            </span>
            <span className="block text-4xl md:text-6xl text-white/80 mt-4">
              While You Sleep
            </span>
          </h1>
          
          <p className="text-xl text-white/70 mb-12 max-w-4xl mx-auto leading-relaxed">
            Apply to <span className="text-cyan-400 font-bold">1,000+ jobs automatically</span> with AI-powered resume optimization 
            and personalized cover letters. Our intelligent system works 24/7 to maximize your 
            job search success across LinkedIn, Indeed, Glassdoor, and more.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16">
                          <Link 
                to="/register" 
                className="group relative bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-400 hover:to-purple-400 text-white px-10 py-4 rounded-2xl text-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-cyan-500/25"
              >
                <span className="relative z-10">Get Started Free</span>
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-purple-600 rounded-2xl blur opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
              </Link>
            <Link 
              to="/login" 
              className="border-2 border-white/30 text-white hover:bg-white/10 px-10 py-4 rounded-2xl text-lg font-semibold transition-all duration-300 transform hover:scale-105 backdrop-blur-sm"
            >
              Sign In
            </Link>
          </div>
          
          {/* 3D Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
            <div 
              className="group relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-2xl p-8 border border-white/20 transform hover:scale-105 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20"
              style={{
                transform: `perspective(1000px) rotateY(${mousePosition.x * 5}deg) rotateX(${mousePosition.y * 5}deg)`
              }}
            >
              <div className="text-4xl font-bold text-cyan-400 mb-2">1,000+</div>
              <div className="text-white/80">Jobs Applied Per Hour</div>
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            <div 
              className="group relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-2xl p-8 border border-white/20 transform hover:scale-105 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20"
              style={{
                transform: `perspective(1000px) rotateY(${mousePosition.x * -5}deg) rotateX(${mousePosition.y * -5}deg)`
              }}
            >
              <div className="text-4xl font-bold text-purple-400 mb-2">24/7</div>
              <div className="text-white/80">Automated Operation</div>
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
          </div>
        </div>

        {/* 3D Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          {[
            {
              icon: "⚡",
              title: "Lightning Fast Applications",
              description: "Apply to thousands of jobs across LinkedIn, Indeed, Glassdoor, and Handshake in minutes, not months.",
              gradient: "from-cyan-500 to-blue-500"
            },
            {
              icon: "🧠",
              title: "AI Resume Enhancement",
              description: "Dynamically optimize your resume for each job using advanced AI models trained on successful applications.",
              gradient: "from-purple-500 to-pink-500"
            },
            {
              icon: "✉️",
              title: "Smart Cover Letters",
              description: "Generate personalized, compelling cover letters tailored to each job description automatically.",
              gradient: "from-green-500 to-emerald-500"
            }
          ].map((feature, index) => (
            <div
              key={index}
              className={`group relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-2xl p-8 border border-white/20 transform hover:scale-105 transition-all duration-500 hover:shadow-2xl transform-gpu ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}
              style={{
                transitionDelay: `${index * 200}ms`,
                transform: `perspective(1000px) rotateY(${mousePosition.x * 3}deg) rotateX(${mousePosition.y * 3}deg) scale(${isLoaded ? 1 : 0.8})`
              }}
            >
              <div className={`w-16 h-16 bg-gradient-to-r ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 text-2xl transform group-hover:rotate-12 transition-transform duration-300`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">{feature.title}</h3>
              <p className="text-white/70 leading-relaxed">{feature.description}</p>
              <div className={`absolute inset-0 bg-gradient-to-r ${feature.gradient} rounded-2xl opacity-0 group-hover:opacity-10 transition-opacity duration-300`}></div>
            </div>
          ))}
        </div>

        {/* 3D Process Steps */}
        <div className="text-center mb-20">
          <h2 className="text-5xl font-bold text-white mb-16">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { step: "1", title: "Upload Resume", desc: "Upload your resume and set preferences", color: "cyan" },
              { step: "2", title: "AI Optimization", desc: "Our AI enhances your resume", color: "purple" },
              { step: "3", title: "Auto Apply", desc: "System applies to thousands of jobs", color: "green" },
              { step: "4", title: "Get Hired", desc: "Track responses and land your dream job", color: "orange" }
            ].map((item, index) => (
              <div
                key={index}
                className={`group relative transform transition-all duration-500 hover:scale-110 ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}
                style={{
                  transitionDelay: `${index * 150}ms`,
                  transform: `perspective(1000px) rotateY(${mousePosition.x * 2}deg) rotateX(${mousePosition.y * 2}deg)`
                }}
              >
                <div className={`w-20 h-20 bg-gradient-to-r from-${item.color}-500 to-${item.color}-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-2xl group-hover:shadow-${item.color}-500/50 transition-all duration-300`}>
                  <span className="text-3xl font-bold text-white">{item.step}</span>
                </div>
                <h3 className="text-lg font-semibold mb-2 text-white">{item.title}</h3>
                <p className="text-white/70">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* 3D CTA Section */}
        <div 
          className="relative bg-gradient-to-r from-cyan-600/20 to-purple-600/20 backdrop-blur-xl rounded-3xl p-12 text-center text-white border border-white/20 transform hover:scale-105 transition-all duration-300 shadow-2xl"
          style={{
            transform: `perspective(1000px) rotateY(${mousePosition.x * 2}deg) rotateX(${mousePosition.y * 2}deg)`
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-3xl"></div>
          <div className="relative z-10">
            <h2 className="text-5xl font-bold mb-4">Ready to Transform Your Job Search?</h2>
            <p className="text-xl mb-8 text-white/80">
              Join thousands of professionals who've automated their way to success
            </p>
            <Link 
              to="/register" 
              className="group relative bg-gradient-to-r from-white to-white/90 text-purple-600 px-10 py-4 rounded-2xl text-lg font-semibold hover:from-white/90 hover:to-white transition-all duration-300 transform hover:scale-105 shadow-2xl"
            >
              <span className="relative z-10">Start Your Journey Now</span>
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-purple-400 rounded-2xl blur opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Home 