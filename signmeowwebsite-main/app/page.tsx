"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Zap, Shield, Mail, Phone, MapPin, Target, TrendingUp, CheckCircle } from "lucide-react"
import { SignMeowLogo } from "@/components/logo"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <SignMeowLogo className="w-10 h-10" />
            <div className="text-2xl font-bold text-slate-800">Sign Meow</div>
          </div>
          <nav className="hidden md:flex space-x-8">
            <a
              href="#home"
              className="text-slate-600 hover:text-slate-900 transition-colors"
              onClick={(e) => {
                e.preventDefault()
                document.getElementById("home")?.scrollIntoView({ behavior: "smooth" })
              }}
            >
              Overview
            </a>
            <a
              href="#features"
              className="text-slate-600 hover:text-slate-900 transition-colors"
              onClick={(e) => {
                e.preventDefault()
                document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })
              }}
            >
              Solution
            </a>
            <a
              href="#about"
              className="text-slate-600 hover:text-slate-900 transition-colors"
              onClick={(e) => {
                e.preventDefault()
                document.getElementById("about")?.scrollIntoView({ behavior: "smooth" })
              }}
            >
              Project Details
            </a>
            <a
              href="#contact"
              className="text-slate-600 hover:text-slate-900 transition-colors"
              onClick={(e) => {
                e.preventDefault()
                document.getElementById("contact")?.scrollIntoView({ behavior: "smooth" })
              }}
            >
              Partnership
            </a>
          </nav>
          <Button className="hidden md:inline-flex">Support Project</Button>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="py-20 px-4">
        <div className="container mx-auto text-center">
          <div className="inline-block bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
            Project Proposal
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-slate-800 mb-6">
            Sign Meow:
            <span className="text-orange-600"> AI-Powered ASL Learning</span>
          </h1>
          <p className="text-xl text-slate-600 mb-8 max-w-3xl mx-auto">
            SignMeow is your AI Powered AI learning buddy that makes ASL learning easy, interactive and fun! :3
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="outline" size="lg" className="text-lg px-8 py-3 bg-transparent">
              View Proposal Details
            </Button>
          </div>
        </div>
      </section>

      {/* Problem & Solution Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-800 mb-4">The Problem & Our Solution</h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto"></p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 mb-16">
            <Card className="border-red-200 bg-red-50">
              <CardHeader>
                <CardTitle className="text-red-800">Current Challenges</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <img
                      src="/images/sad-cat.png"
                      alt="Sad cat representing learning challenges"
                      className="w-24 h-24 object-contain"
                    />
                  </div>
                  <ul className="space-y-2 text-red-700 flex-1">
                    <li className="flex items-start space-x-2">
                      <span className="text-red-500 mt-1 text-sm">•</span>
                      <span className="text-sm leading-relaxed">Limited access to qualified ASL instructors</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-red-500 mt-1 text-sm">•</span>
                      <span className="text-sm leading-relaxed">No real-time feedback on sign accuracy</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-red-500 mt-1 text-sm">•</span>
                      <span className="text-sm leading-relaxed">Difficulty tracking learning progress</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <span className="text-red-500 mt-1 text-sm">•</span>
                      <span className="text-sm leading-relaxed">Expensive traditional learning methods</span>
                    </li>
                  </ul>
                </div>
              </CardContent>
            </Card>

            <Card className="border-green-200 bg-green-50">
              <CardHeader>
                <CardTitle className="text-green-800">Our Innovation</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <img
                      src="/images/happy-cat.png"
                      alt="Happy cat representing innovative solutions"
                      className="w-24 h-24 object-contain"
                    />
                  </div>
                  <ul className="space-y-2 text-green-700 flex-1">
                    <li className="flex items-start space-x-2">
                      <CheckCircle className="text-green-500 mt-1 h-4 w-4 flex-shrink-0" />
                      <span className="text-sm leading-relaxed">Computer vision reads hand signs instantly</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <CheckCircle className="text-green-500 mt-1 h-4 w-4 flex-shrink-0" />
                      <span className="text-sm leading-relaxed">Real-time translation to English text</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <CheckCircle className="text-green-500 mt-1 h-4 w-4 flex-shrink-0" />
                      <span className="text-sm leading-relaxed">AI-powered progress tracking system</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <CheckCircle className="text-green-500 mt-1 h-4 w-4 flex-shrink-0" />
                      <span className="text-sm leading-relaxed">LCD displays for guided practice</span>
                    </li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
                  <Zap className="h-6 w-6 text-orange-600" />
                </div>
                <CardTitle>Computer Vision Technology</CardTitle>
                <CardDescription>
                  Advanced algorithms instantly recognize hand signs and translate them into English using ASL
                  dictionaries.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <Shield className="h-6 w-6 text-blue-600" />
                </div>
                <CardTitle>Interactive LCD Displays</CardTitle>
                <CardDescription>
                  Practice sentences displayed on LCD screens provide clear learning objectives while our system tracks
                  your signing accuracy.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                  <TrendingUp className="h-6 w-6 text-green-600" />
                </div>
                <CardTitle>AI Progress Analytics</CardTitle>
                <CardDescription>
                  Machine learning algorithms track learning patterns, identify improvement areas, and adapt difficulty
                  levels for optimal progress.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>
      {/* Project Details Section */}
      <section id="about" className="py-20 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-slate-800 mb-6">Project Implementation</h2>
              <p className="text-lg text-slate-600 mb-6">
                Sign Meow represents a breakthrough in ASL education technology. Our proposed system combines computer
                vision, machine learning, and interactive hardware to create an unprecedented learning experience that
                serves both beginners and experienced signers.
              </p>
              <p className="text-lg text-slate-600 mb-8">
                Our goal is to make ASL learning accessible, affordable, and effective for everyone.
              </p>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-slate-800">Key Milestones</h3>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-slate-600">Computer vision prototype development</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span className="text-slate-600">LCD display integration and testing</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Target className="h-5 w-5 text-orange-600" />
                    <span className="text-slate-600">AI progress tracking system</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Target className="h-5 w-5 text-orange-600" />
                    <span className="text-slate-600">Beta testing with ASL community</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Target className="h-5 w-5 text-orange-600" />
                    <span className="text-slate-600">Commercial product launch</span>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <img
                src="/placeholder.svg?height=500&width=600"
                alt="Project timeline"
                className="rounded-lg shadow-lg"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Partnership Section */}
      <section id="contact" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-800 mb-4">Partner With Us</h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              Join us in revolutionizing ASL education and our vision of making sign language learning accessible to
              everyone.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <Card>
                <CardHeader>
                  <CardTitle>Get Involved</CardTitle>
                  <CardDescription>Interested in supporting or partnering with SignMeow? Contact us!</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-4">
                    <Input placeholder="First Name" />
                    <Input placeholder="Last Name" />
                  </div>
                  <Input placeholder="Email Address" type="email" />
                  <Input placeholder="Organization" />
                  <Textarea placeholder="How would you like to get involved?" rows={4} />
                  <Button className="w-full">Submit Partnership Inquiry</Button>
                </CardContent>
              </Card>
            </div>

            <div>
              <h4 className="text-lg font-semibold text-slate-800 mb-4">Contact Information</h4>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <Mail className="h-5 w-5 text-blue-600" />
                  <span>partnerships@signmeow.com</span>
                </div>
                <div className="flex items-center space-x-3">
                  <Phone className="h-5 w-5 text-blue-600" />
                  <span>+1 (555) 123-4567</span>
                </div>
                <div className="flex items-center space-x-3">
                  <MapPin className="h-5 w-5 text-blue-600" />
                  <span>Toronto Metropolitan University</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-800 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="text-2xl font-bold mb-4">Sign Meow</div>
              <p className="text-slate-300">
                A revolutionary project proposal for AI-powered ASL education using computer vision and interactive
                learning technology.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Project Components</h4>
              <ul className="space-y-2 text-slate-300">
                <li>Computer Vision System</li>
                <li>LCD Practice Displays</li>
                <li>AI Progress Tracking</li>
                <li>ASL Translation Engine</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Get Involved</h4>
              <ul className="space-y-2 text-slate-300">
                <li>Partnership Opportunities</li>
                <li>Investment Information</li>
                <li>Technical Collaboration</li>
                <li>Community Feedback</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-slate-300">
                <li>Project Proposal</li>
                <li>Technical Specifications</li>
                <li>Market Research</li>
                <li>Development Timeline</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-700 mt-8 pt-8 text-center text-slate-300">
            <p>&copy; 2025 Sign Meow Project. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
