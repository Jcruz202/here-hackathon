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
    <Box
      width="100vw"
      height="100vh"
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
    >
      <Button variant="h4" onClick={() => {handleNavigation()}}>AI customer support</Button>
    </Box>
  );
}