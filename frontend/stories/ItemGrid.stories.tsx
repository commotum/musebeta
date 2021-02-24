import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { ItemGrid } from '../components/ItemGrid'
import { getItems } from '../utils/mock'

storiesOf('components/ItemGrid', module).add('default', () => (
  <ItemGrid
    items={getItems(10)}
    onTrain={action('onTrain')}
    onDelete={action('OnDelete')}
    onGenerate={action('onGenerate')}
    onHistory={action('onHistory')}
    onRename={action('nnRename')}
  />
))
