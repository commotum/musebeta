import * as React from 'react'
import { storiesOf } from '@storybook/react'

import { Button, SecButton } from '../../components/common/Button'

storiesOf('common/Button', module)
  .add('primary', () => <Button>Button</Button>)
  .add('secondary', () => <SecButton>Button</SecButton>)
