import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { Item } from '../components/Item'

storiesOf('components/Item', module).add('default', () => (
  <Item
    title="OpenAI 124M"
    onTrain={action('onTrain')}
    onDelete={action('OnDelete')}
    onGenerate={action('onGenerate')}
    onHistory={action('onHistory')}
    onRename={action('nnRename')}
  />
))
