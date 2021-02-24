import * as React from 'react'
import { storiesOf } from '@storybook/react'
import styled from 'styled-components'

import { LoadingText } from '../components/LoadingText'

const Wrap = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
`

const SLoadingText = styled(LoadingText)`
  width: 40%;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
`

storiesOf('components/LoadingText', module)
  .add('default', () => (
    <Wrap>
      <SLoadingText
        text={[
          'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce faucibus, magna ac consectetur suscipit, elit magna fermentum ante, quis hendrerit lectus urna sodales neque. Nullam pellentesque, risus quis convallis vehicula, odio diam fringilla lorem, vel dapibus ex nisi venenatis libero. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras placerat cursus nibh eget venenatis. Suspendisse ut sapien dictum, malesuada mauris et, iaculis risus. Nam ullamcorper dolor in massa semper, eu lobortis ex blandit. Vestibulum placerat vestibulum neque, aliquet viverra ligula luctus vel. Integer aliquet tincidunt sapien, vel tincidunt mi volutpat in. Donec at pellentesque ex, non scelerisque metus. Pellentesque iaculis porta mi nec sodales. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Mauris blandit ex est, eleifend tristique risus iaculis vitae. Fusce augue nisi, dapibus in odio at, consectetur volutpat velit. Pellentesque porta orci arcu, at volutpat turpis suscipit eu. Morbi nec felis eget elit efficitur condimentum id vel nisl.',
        ]}
      />
    </Wrap>
  ))
  .add('long text', () => (
    <Wrap>
      <SLoadingText
        text={[
          'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce faucibus, magna ac consectetur suscipit, elit magna fermentum ante, quis hendrerit lectus urna sodales neque. Nullam pellentesque, risus quis convallis vehicula, odio diam fringilla lorem, vel dapibus ex nisi venenatis libero. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras placerat cursus nibh eget venenatis. Suspendisse ut sapien dictum, malesuada mauris et, iaculis risus. Nam ullamcorper dolor in massa semper, eu lobortis ex blandit. Vestibulum placerat vestibulum neque, aliquet viverra ligula luctus vel. Integer aliquet tincidunt sapien, vel tincidunt mi volutpat in. Donec at pellentesque ex, non scelerisque metus. Pellentesque iaculis porta mi nec sodales. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Mauris blandit ex est, eleifend tristique risus iaculis vitae. Fusce augue nisi, dapibus in odio at, consectetur volutpat velit. Pellentesque porta orci arcu, at volutpat turpis suscipit eu. Morbi nec felis eget elit efficitur condimentum id vel nisl. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce faucibus, magna ac consectetur suscipit, elit magna fermentum ante, quis hendrerit lectus urna sodales neque. Nullam pellentesque, risus quis convallis vehicula, odio diam fringilla lorem, vel dapibus ex nisi venenatis libero. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras placerat cursus nibh eget venenatis. Suspendisse ut sapien dictum, malesuada mauris et, iaculis risus. Nam ullamcorper dolor in massa semper, eu lobortis ex blandit. Vestibulum placerat vestibulum neque, aliquet viverra ligula luctus vel. Integer aliquet tincidunt sapien, vel tincidunt mi volutpat in. Donec at pellentesque ex, non scelerisque metus. Pellentesque iaculis porta mi nec sodales. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Mauris blandit ex est, eleifend tristique risus iaculis vitae. Fusce augue nisi, dapibus in odio at, consectetur volutpat velit. Pellentesque porta orci arcu, at volutpat turpis suscipit eu. Morbi nec felis eget elit efficitur condimentum id vel nisl. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce faucibus, magna ac consectetur suscipit, elit magna fermentum ante, quis hendrerit lectus urna sodales neque. Nullam pellentesque, risus quis convallis vehicula, odio diam fringilla lorem, vel dapibus ex nisi venenatis libero. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras placerat cursus nibh eget venenatis. Suspendisse ut sapien dictum, malesuada mauris et, iaculis risus. Nam ullamcorper dolor in massa semper, eu lobortis ex blandit. Vestibulum placerat vestibulum neque, aliquet viverra ligula luctus vel. Integer aliquet tincidunt sapien, vel tincidunt mi volutpat in. Donec at pellentesque ex, non scelerisque metus. Pellentesque iaculis porta mi nec sodales. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Mauris blandit ex est, eleifend tristique risus iaculis vitae. Fusce augue nisi, dapibus in odio at, consectetur volutpat velit. Pellentesque porta orci arcu, at volutpat turpis suscipit eu. Morbi nec felis eget elit efficitur condimentum id vel nisl.',
        ]}
      />
    </Wrap>
  ))
