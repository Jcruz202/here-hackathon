'use client'
import { Box, Stack, TextField, Button, Typography } from "@mui/material";
import { useRouter } from "next/navigation"
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const router = useRouter();

  const handleNavigation = () => {
    router.push('/chat');
  };


  return (
    <Box>
      {/* First Section */}
      <Box
        width="100vw"
        height="100vh"
        display="flex"
        justifyContent="flex-end"
        alignItems="center"
        bgcolor="#f0f0f0" // Optional: background color for visual separation
      >
        <Typography
          variant="h4"
          sx={{
            paddingRight: '10%', // Adjust this value to move the text more to the right or left
            maxWidth: '60%', // Ensure the text doesn't stretch too wide
            textAlign: 'center',
            color: '#333', // Dark grey color for better contrast
            fontWeight: 500, // Medium font weight
            fontSize: 80,
          }}
        >
          {"Welcome to Roundabout Locator"}
        </Typography>
      </Box>

      {/* Second Section */}
      <Box
        width="100vw"
        height="100vh"
        display="flex"
        justifyContent="center" // Center text horizontally
        alignItems="center" // Center text vertically
        bgcolor="#e0e0e0" // Optional: background color for visual separation
      >
        <Stack
          direction="column"
          justifyContent="center" // Center content vertically
          alignItems="flex-start" // Align items to the start (left)
          sx={{ width: '100%', paddingLeft: '10%' }} // Adjust padding as needed
        >
          <Typography
            variant="h6"
            sx={{
              maxWidth: '50%',
              textAlign: 'left', // Align text to the left
              color: '#333',
              fontSize: 24, // Adjust font size as needed
            }}
          >
            Using a trained model, we can calculate whether the given parallels...
          </Typography>
        </Stack>
      </Box>

      {/* Third section */}
      <Box
        width="100vw"
        height="100vh"
        display="flex"
        justifyContent="center" // Center text horizontally
        alignItems="center" // Center text vertically
        bgcolor="#f0f0f0" // Optional: background color for visual separation
      >
        <Stack
          direction="column"
          justifyContent="center" // Center content vertically
          alignItems="flex-start" // Align items to the start (left)
          sx={{ width: '100%', paddingLeft: '10%' }} // Adjust padding as needed
        >
          <Typography
            variant="h6"
            sx={{
              maxWidth: '50%',
              textAlign: 'left', // Align text to the left
              color: '#333',
              fontSize: 24, // Adjust font size as needed
            }}
          >
            Put text here
          </Typography>
        </Stack>
      </Box>
    </Box>
  );
}