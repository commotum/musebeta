import { configure } from '@storybook/react'
import { addDecorator } from '@storybook/react'
import { withThemesProvider } from 'storybook-addon-styled-component-theme'
import { theme } from '../themes'
import React from 'react'
import * as nextImage from 'next/image'

Object.defineProperty(nextImage, 'default', {
  configurable: true,
  value: (props) => {
    return React.createElement('img', props)
  },
})

const req = require.context('../stories', true, /.stories.tsx$/)
function loadStories() {
  req.keys().forEach(filename => req(filename))
}

addDecorator(withThemesProvider([theme]))
configure(loadStories, module)

