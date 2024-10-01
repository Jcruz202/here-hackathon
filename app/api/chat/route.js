import {NextResponse} from 'next/server' // Import NextResponse from Next.js for handling responses
import OpenAI from 'openai' // Import OpenAI library for interacting with the OpenAI API

// System prompt for the AI, providing guidelines on how to respond to users
const systemPrompt = `You are a customer support AI for HereTechnology API, a platform that provide a 
variety of location-based data and services, including routing, traffic, and mapping. Your role is to:

Answer questions about 
Routing API: Calculates routes between locations, including turn-by-turn instructions. Users can specify preferences like fastest or shortest routes, and restrictions like tolls and highways.
Traffic API: Provides real-time traffic flow and incident information, including speed, jam factor, and traffic incident type and location.
Raster Tile API: Provides bitmap images for web and mobile screens, with customizable features like congestion zones and points of interest.
Lanes API: Provides information about roads and lanes, which can be used for precise lane-level guidance.
Data Processing Library (DPL): Compiles maps incrementally when new source data is released. 
Other HERE Technologies products include: Location Services, Maps Geocoding and Search Routing, Fleet Telematics, and HERE SDK.
Provide technical support for using the platform

Explain how the app works
Assist with account-related issues
Handle inquiries about pricing and plans

Be concise, friendly, and professional. If you can't resolve an issue, offer to escalate it to a human support agent. Prioritize user privacy and data security in your responses.`


// POST function to handle incoming requests
export async function POST(req) {
  const openai = new OpenAI() // Create a new instance of the OpenAI client
  const data = await req.json() // Parse the JSON body of the incoming request

  // Create a chat completion request to the OpenAI API
  const completion = await openai.chat.completions.create({
    messages: [{role: 'system', content: systemPrompt}, ...data], // Include the system prompt and user messages
    model: 'gpt-4o', // Specify the model to use
    stream: true, // Enable streaming responses
  })

  // Create a ReadableStream to handle the streaming response
  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder() // Create a TextEncoder to convert strings to Uint8Array
      try {
        // Iterate over the streamed chunks of the response
        for await (const chunk of completion) {
          const content = chunk.choices[0]?.delta?.content // Extract the content from the chunk
          if (content) {
            const text = encoder.encode(content) // Encode the content to Uint8Array
            controller.enqueue(text) // Enqueue the encoded text to the stream
          }
        }
      } catch (err) {
        controller.error(err) // Handle any errors that occur during streaming
      } finally {
        controller.close() // Close the stream when done
      }
    },
  })

  return new NextResponse(stream) // Return the stream as the response
}