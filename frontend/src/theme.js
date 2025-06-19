// src/theme.js
import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  styles: {
    global: {
      body: {
        bg: '#ffffff',
      },
    },
  },
  components: {
    Button: {
      baseStyle: {
        _hover: {
          bg: '#e14e2f',
        },
      },
      variants: {
        solid: {
          bg: '#ff5c36',
          color: 'white',
          _hover: {
            bg: '#e14e2f',
          },
        },
      },
    },
  },
});

export default theme;
